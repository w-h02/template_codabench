from pathlib import Path

try:
    import docker
except ImportError:
    raise ImportError(
        "The 'docker' package is required to run this script. "
        "Please install it using 'pip install docker'."
    )

REPO  = Path(__file__).resolve().parent.parent
IMAGE = "rayenmansour/crystal-challenge:v2"


def remove_container(client, name):
    """Remove a container by name if it exists (handles the 409 Conflict error)."""
    try:
        container = client.containers.get(name)
        container.remove(force=True)
        print(f"  Removed existing container: {name}")
    except docker.errors.NotFound:
        pass  # Container doesn't exist, nothing to do


if __name__ == "__main__":
    client = docker.from_env()
    print("Docker client initialized successfully.")

    # Create output directories if they don't exist
    (REPO / "ingestion_res").mkdir(exist_ok=True)
    (REPO / "scoring_res").mkdir(exist_ok=True)

    # ── Ingestion ─────────────────────────────────────────────────────────────
    print("\nRunning ingestion...")
    remove_container(client, "ingestion")
    logs = client.containers.run(
        image=IMAGE,
        command="python3 /app/ingestion_program/ingestion.py",
        remove=True,
        name="ingestion",
        user="root",
        volumes=[
            f"{REPO}/ingestion_program:/app/ingestion_program",
            f"{REPO}/dev_phase/input_data:/app/input_data",
            f"{REPO}/ingestion_res:/app/output",
            f"{REPO}/solution:/app/ingested_program",
        ]
    )
    print(logs.decode("utf-8"))

    # ── Scoring ───────────────────────────────────────────────────────────────
    print("\nRunning scoring...")
    remove_container(client, "scoring")
    logs = client.containers.run(
        image=IMAGE,
        command="python3 /app/scoring_program/scoring.py",
        remove=True,
        name="scoring",
        user="root",
        volumes=[
            f"{REPO}/scoring_program:/app/scoring_program",
            f"{REPO}/dev_phase/reference_data:/app/input/ref",
            f"{REPO}/ingestion_res:/app/input/res",
            f"{REPO}/scoring_res:/app/output",
        ]
    )
    print(logs.decode("utf-8"))
    print("Done.")