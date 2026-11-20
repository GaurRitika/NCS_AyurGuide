from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import router
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Rebuild the RAG vector store on startup if it's empty. This matters
    # on hosts with ephemeral disks (e.g. Render's free tier wipes disk on
    # every redeploy) - the knowledge base's real source of truth is the
    # .txt files committed to the repo, and the vector store is a
    # regenerable artifact rebuilt from them, not something we rely on
    # persisting across deploys. If the disk did survive (e.g. a plain
    # restart), this is a fast no-op.
    try:
        from .services.rag.ingest import build_knowledge_base
        build_knowledge_base(force=False)
    except Exception as e:
        # A knowledge-base build failure should not prevent the API from
        # starting - RAG-dependent endpoints will fall back gracefully
        # (see RecommendationEngine._get_reference_material), the rest
        # of the app still works without it.
        logger.error(f"RAG knowledge base build failed on startup: {e}")
    yield


app = FastAPI(title="Ayurvedic Consultation API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000" ,
                #    'https://frontend-dot-ayurguide-451219.uc.r.appspot.com' 
                "https://mydva-deployment.vercel.app"
                   ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Remove the prefix here - don't include it in app.include_router
app.include_router(router)  # Remove prefix="/api/v1"
