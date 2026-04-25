import uvicorn
import os
from app.config import get_settings

def main():
    settings = get_settings()
    
    # Configure reload excludes to prevent loops when database or index files change
    reload_excludes = [
        "app/data/*",
        "app/uploads/*",
        "*.db",
        "*.index",
        "*.json"
    ]
    
    print(f"Starting {settings.app_name} in development mode...")
    print(f"Excluding from reload: {', '.join(reload_excludes)}")
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_excludes=reload_excludes,
        log_level="info"
    )

if __name__ == "__main__":
    main()
