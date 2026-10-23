# Architecture and development constraints

This release is a vertical slice. It deliberately avoids untested infrastructure dependencies. The browser calls POST /api/jobs, Node persists a JSON job, invokes an optional OpenAI-compatible text completion, spawns Python, Pillow renders visual cards, and FFmpeg produces an MP4. GET /api/jobs exposes status and /api/videos/:id.mp4 serves output with byte-range support.

Important limitations: no auth, single worker, no cancellation, no resilient multi-process queue, no scene animation, no TTS, no fact verification, and no arbitrary network-safe URL ingestion. Use only on localhost. Provider errors are surfaced rather than silently replaced with fake AI results. Scenes are bounded and length-validated. Generated content is text-only; procedural media is deterministic.

Future architecture: move scene schemas into a shared TypeScript package, adopt Remotion compositions, use BullMQ and Redis for jobs, MongoDB for metadata, S3-compatible object storage for video, and add separate rendering workers. Retain the same UI concepts while replacing the minimal API.