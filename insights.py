from flask import request, jsonify
from datetime import datetime, timedelta
import models
from app import app


def _get_user_insights(user_id):
    user = models.User.query.get(user_id)
    if not user:
        return None, jsonify({'error': 'User not found'}), 404

    sessions = models.Session.query.filter_by(user_id=user_id).all()
    if not sessions:
        return None, jsonify({"message": "No session found for this user"}), 404

    durations = [s.duration_min for s in sessions if getattr(s, 'duration_min', None) is not None]
    avg_session_length = sum(durations) / len(durations) if durations else 0

    time_ranges = {
        "Night": "00:00-06:00",
        "Morning": "06:00-12:00",
        "Afternoon": "12:00-18:00",
        "Evening": "18:00-24:00",
    }

    buckets = {"Night": [], "Morning": [], "Afternoon": [], "Evening": []}
    for session in sessions:
        if session.session_start:
            hour = session.session_start.hour
            if 0 <= hour < 6:
                buckets["Night"].append(session.duration_min)
            elif 6 <= hour < 12:
                buckets["Morning"].append(session.duration_min)
            elif 12 <= hour < 18:
                buckets["Afternoon"].append(session.duration_min)
            else:
                buckets["Evening"].append(session.duration_min)

    best_bucket = None
    best_avg = 0
    for bucket, values in buckets.items():
        if values:
            bucket_avg = sum(values) / len(values)
            if bucket_avg > best_avg:
                best_avg = bucket_avg
                best_bucket = bucket

    today = datetime.utcnow().date()
    recent_start = today - timedelta(days=6)
    previous_start = today - timedelta(days=13)
    baseline_start = today - timedelta(days=29)

    recent_sessions = [s for s in sessions if recent_start <= s.date <= today]
    previous_sessions = [s for s in sessions if previous_start <= s.date < recent_start]
    baseline_sessions = [s for s in sessions if baseline_start <= s.date <= today]

    def avg_duration(session_list):
        values = [s.duration_min for s in session_list if getattr(s, 'duration_min', None) is not None]
        return sum(values) / len(values) if values else 0

    recent_avg = avg_duration(recent_sessions)
    previous_avg = avg_duration(previous_sessions)
    baseline_avg = avg_duration(baseline_sessions)

    if previous_avg <= 0:
        trend = "Improving" if recent_avg > 0 else "Stable"
    else:
        if recent_avg > previous_avg * 1.4:
            trend = "Improving"
        elif recent_avg < previous_avg * 0.7:
            trend = "Declining"
        else:
            trend = "Stable"

    def active_days(session_list):
        return len(set(session.date for session in session_list if session.date))

    def late_night_count(session_list):
        count = 0
        for session in session_list:
            if session.session_start and (session.session_start.hour < 4 or session.session_start.hour >= 21):
                count += 1
        return count

    recent_active_days = active_days(recent_sessions)
    recent_late_nights = late_night_count(recent_sessions)

    burnout_score = 0
    burnout_signals = []
    if recent_active_days >= 6:
        burnout_score += 25
        burnout_signals.append("Active on most days in the last week")
    if baseline_avg > 0 and recent_avg > baseline_avg * 1.3:
        burnout_score += 25
        burnout_signals.append("Recent sessions length is significantly above baseline")
    if recent_late_nights >= 2:
        burnout_score += 20
        burnout_signals.append("Multiple late-night sessions in the last week")
    rest_days = 7 - recent_active_days
    if rest_days <= 1:
        burnout_score += 15
        burnout_signals.append("Very few rest days in last week")
    if baseline_avg > 0 and recent_avg < baseline_avg * 0.8 and recent_active_days >= 5:
        burnout_score += 15
        burnout_signals.append("Possible fatigue pattern: High activity with shorter sessions")

    if burnout_score >= 70:
        burnout_level = "High"
    elif burnout_score >= 35:
        burnout_level = "Medium"
    else:
        burnout_level = "Low"

    recommended_duration = round(avg_session_length)
    if burnout_level == "High":
        recommended_duration = max(20, round(avg_session_length * 0.7))
    elif burnout_level == "Medium":
        recommended_duration = max(25, round(avg_session_length * 0.87))

    recommendation = {
        "recommended_start_window": time_ranges.get(best_bucket),
        "recommended_duration_minutes": recommended_duration,
        "focus_note": f"You tend to work best during the {best_bucket.lower() if best_bucket else 'day'}.",
    }

    return {
        "user_id": user_id,
        "avg_session_length": avg_session_length,
        "best_bucket": best_bucket,
        "best_bucket_average": best_avg,
        "time_ranges": time_ranges,
        "recent_avg": recent_avg,
        "previous_avg": previous_avg,
        "baseline_avg": baseline_avg,
        "trend": trend,
        "recent_active_days": recent_active_days,
        "recent_late_nights": recent_late_nights,
        "burnout_score": burnout_score,
        "burnout_level": burnout_level,
        "burnout_signals": burnout_signals,
        "recommendation": recommendation,
    }, None, None


@app.route('/insights/personal-baseline/<user_id>', methods=['GET'])
def personal_baseline(user_id):
    insights, error_response, status_code = _get_user_insights(user_id)
    if error_response:
        return error_response, status_code

    return jsonify({
        "user_id": insights["user_id"],
        "best_time_of_day_to_work": {
            "label": insights["best_bucket"],
            "time_range": insights["time_ranges"].get(insights["best_bucket"]),
            "average_session_length": round(insights["best_bucket_average"], 2) if insights["best_bucket"] else 0,
        },
        "average_session_length": {"minutes": round(insights["avg_session_length"], 2)},
        "productivity_pattern_over_time": {"trend": insights["trend"]},
        "burnout_risk": {
            "level": insights["burnout_level"],
            "score": insights["burnout_score"],
            "signals": insights["burnout_signals"],
        },
        "next_session_recommendation": insights["recommendation"],
    }), 200


@app.route('/insights/burnout/<user_id>', methods=['GET'])
def burnout_insight(user_id):
    insights, error_response, status_code = _get_user_insights(user_id)
    if error_response:
        return error_response, status_code

    return jsonify({
        "user_id": insights["user_id"],
        "burnout_level": insights["burnout_level"],
        "score": insights["burnout_score"],
        "signals": insights["burnout_signals"],
        "recent_average_minutes": round(insights["recent_avg"], 2),
        "baseline_average_minutes": round(insights["baseline_avg"], 2),
        "recent_active_days": insights["recent_active_days"],
        "recent_late_nights": insights["recent_late_nights"],
    }), 200


@app.route('/insights/recommendations/<user_id>', methods=['GET'])
def recommendations(user_id):
    insights, error_response, status_code = _get_user_insights(user_id)
    if error_response:
        return error_response, status_code

    return jsonify({
        "user_id": insights["user_id"],
        "recommended_start_window": insights["recommendation"]["recommended_start_window"],
        "recommended_duration_minutes": insights["recommendation"]["recommended_duration_minutes"],
        "notes": [
            "Maintain your current session lengths and consistency."
            if insights["burnout_level"] == "Low"
            else "Try shorter focused sessions (50-90 minutes) to reduce fatigue."
            if insights["burnout_level"] == "High"
            else "Consider increasing session length slightly to deepen focus."
        ],
        "best_time_bucket": insights["best_bucket"],
        "best_bucket_average_minutes": round(insights["best_bucket_average"], 2),
    }), 200
