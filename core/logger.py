import inspect
import json
import uuid
import logging
import sys
from pathlib import Path
from datetime import datetime, timezone

import streamlit as st


def _now():
    return datetime.now(timezone.utc).isoformat()

def _page_name():

    for frame in inspect.stack():

        path = Path(frame.filename)

        # skip logger.py itself
        if path.name == "logger.py":
            continue

        # skip anything in core/
        if "core" in path.parts:
            continue

        page = path.stem

        # remove Streamlit page numbering
        if "_" in page:
            page = page.split("_", 1)[1]

        return page

    return "Unknown"


def _session_id():

    if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid.uuid4())

    return st.session_state["session_id"]


def _write(event_type, page, params):

    record = {
        "timestamp": _now(),
        "event": event_type,
        "page": page,
        "session_id": _session_id(),
        "params": params,
    }

    #print(json.dumps(record))
    logger.info(json.dumps(record))


def log_page_visit():

    page = _page_name()

#    key = f"visit_logged_{page}"
#    if key in st.session_state:
#        return
#    st.session_state[key] = True

    _write(
        event_type="page_visit",
        page=page,
        params=dict(st.query_params),
    )

def log_filter_change(filters):

    current = json.dumps(filters, sort_keys=True)

    last = st.session_state.get("last_filters")

    if current == last:
        return

    st.session_state["last_filters"] = current

    _write(
        event_type="filter_change",
        page=_page_name(),
        params=filters,
    )

logger = logging.getLogger("ev-market-explorer")

logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)

handler.setFormatter(
    logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s"
    )
)

if not logger.handlers:
    logger.addHandler(handler)

logger.propagate = False

#logger.info("Search page loaded")
#logger.warning("Warning test")
#logger.error("Error test")