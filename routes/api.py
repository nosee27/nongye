from flask import Blueprint, request, jsonify
from models import db, ChatRecord, Feedback
from agents import AGENT_MAP
from config import Config
import uuid

api_bp = Blueprint("api", __name__, url_prefix="/api")

AGENT_PRIORITY = ["病虫害诊断", "市场行情", "产销对接", "种植规划"]

def dispatch(user_msg: str):
    for name in AGENT_PRIORITY:
        cls = AGENT_MAP.get(name)
        if not cls:
            continue
        agent = cls(Config.OPENAI_API_KEY, Config.OPENAI_BASE_URL, Config.MODEL_NAME)
        if agent.route(user_msg):
            return agent
    return AGENT_MAP["种植规划"](Config.OPENAI_API_KEY, Config.OPENAI_BASE_URL, Config.MODEL_NAME)

@api_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_msg = data.get("message", "").strip()
    session_id = data.get("session_id", "") or str(uuid.uuid4())[:8]

    if not user_msg:
        return jsonify({"error": "消息不能为空"}), 400

    agent = dispatch(user_msg)
    reply = agent.chat(user_msg)

    record = ChatRecord(
        session_id=session_id,
        agent_name=agent.name,
        user_msg=user_msg,
        agent_reply=reply
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({
        "session_id": session_id,
        "agent_name": agent.name,
        "reply": reply,
        "status": "ok"
    })

@api_bp.route("/agents", methods=["GET"])
def list_agents():
    return jsonify({
        "agents": [
            {"name": "种植规划Agent", "icon": "🌱", "desc": "制定种植计划、农事安排"},
            {"name": "病虫害诊断Agent", "icon": "🐛", "desc": "识别病虫害、提供防治方案"},
            {"name": "市场行情Agent", "icon": "📈", "desc": "查询农产品价格与走势"},
            {"name": "产销对接Agent", "icon": "🚚", "desc": "对接收购商与销售渠道"},
        ]
    })

@api_bp.route("/history/<session_id>", methods=["GET"])
def history(session_id):
    records = ChatRecord.query.filter_by(session_id=session_id).order_by(ChatRecord.created_at.asc()).all()
    return jsonify({
        "data": [
            {"agent": r.agent_name, "user": r.user_msg, "reply": r.agent_reply,
             "time": r.created_at.strftime("%Y-%m-%d %H:%M:%S")}
            for r in records
        ]
    })

@api_bp.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json() or {}
    fb = Feedback(
        session_id=data.get("session_id", ""),
        agent_name=data.get("agent_name", ""),
        rating=data.get("rating"),
        content=data.get("content", "")
    )
    db.session.add(fb)
    db.session.commit()
    return jsonify({"status": "ok"})
