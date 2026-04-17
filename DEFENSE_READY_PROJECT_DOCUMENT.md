# Defense-Ready Project Document

## Project Identity

This system is a pothole reporting and road-risk management platform with four concrete layers:
1. A React frontend for citizen and authority workflows.
2. A FastAPI backend for authentication, reporting, clustering, and repair management.
3. MongoDB for persistence, indexing, and aggregation.
4. An H3-based geospatial engine for risk-zone grouping.

The implementation basis is visible in the current codebase through the frontend router and API client, the backend FastAPI entrypoint, the report, zone, repair, and auth routes, and the CV/geospatial services.

## Section 1: Problem Formalization

### What is implemented

The operational decision problem is binary pothole verification:

$x = I$

where $I$ is an uploaded road image, and the model outputs

$f(I) = \hat{y}, \quad \hat{y} \in [0,1]$

with a thresholded decision

$y = \mathbb{1}[\hat{y} \ge \tau], \quad y \in \{0,1\}$

In this project, $y=1$ means the image is treated as containing a pothole and $y=0$ means it is not confirmed.

### How it works

The backend currently performs a computer-vision verification pass on the uploaded image before persisting the report. The verification score is produced from multiple image cues: dark-region ratio, edge density, local texture variance, contrast, and hole-like region evidence. The score is then normalized to a 0-100 confidence scale and thresholded to decide whether the report is verified, rejected, or left pending for manual review.

For a binary classification objective, the mathematically appropriate loss is binary cross-entropy:

$$
L(\theta) = -\frac{1}{N} \sum_{i=1}^{N} \left[y_i \log(\hat{y}_i) + (1-y_i)\log(1-\hat{y}_i)\right]
$$

Although the live API does not train a neural classifier online, BCE is the correct objective for any supervised pothole classifier used in this system because the label space is binary and the output is probabilistic.

### Why this approach was chosen

Binary classification is the correct formalization because the system is not trying to estimate pothole depth, area, or severity directly at the first decision point. The first technical question is whether the image is sufficiently consistent with pothole damage to enter the reporting pipeline. That makes the initial task a yes/no verification problem.

### Why alternatives were not chosen

Regression was rejected for the first-stage decision because it would predict a continuous severity score without solving the primary gatekeeping question. Multi-class classification was also unnecessary at the front gate because the operational workflow only needs a binary verification before later human or authority review. Pure object detection is useful, but the current production path is optimized for image-level verification rather than box-level localization.

### Real-world implication of errors

False positives create wasted field inspection, unnecessary risk-zone inflation, and possible repair misallocation. False negatives are worse operationally because real potholes are missed, creating unresolved safety hazards, vehicle damage risk, and delayed municipal response. In this project, recall on true potholes matters more than perfect specificity because the cost of missing a road defect is higher than the cost of reviewing a small number of extra reports.

## Section 2: Real-World Context

### What is implemented

The system supports citizen reporting, authority review, pothole clustering, and repair action tracking. A citizen uploads an image and coordinates; the backend verifies the image, stores the report, and later groups verified reports into risk zones for authority action.

### How it works

The frontend exposes user flows for login, registration, report submission, recent reports, and authority dashboard review. The backend uses authenticated API endpoints to store reports, serve aggregated risk zones, and create repair actions. The geospatial layer turns isolated pothole observations into actionable clusters.

### Why this approach was chosen

Smart-city infrastructure needs low-friction reporting and fast triage. A citizen-facing UI reduces reporting latency. An authority dashboard converts many raw observations into a manageable operational queue. H3-based clustering converts individual points into city-level maintenance priorities.

### Why alternatives were not chosen

A standalone manual hotline or spreadsheet workflow is too slow, unstructured, and difficult to spatially analyze. A fully autonomous closed-loop repair system was not chosen because road maintenance still requires human validation, budgeting, and dispatch coordination. The chosen design balances automation with accountable human review.

### Economic and safety impact

Earlier pothole detection reduces vehicle damage claims, lowers accident probability, and decreases emergency repair cost escalation. For governments, the system supports evidence-based maintenance planning, service-level monitoring, and prioritization of constrained repair budgets.

### Autonomous vehicle relevance

Road-surface defects are relevant to autonomy because perception stacks and planning layers assume lane continuity and drivable terrain. A pothole mapping system does not replace an AV perception stack, but it provides infrastructure intelligence that can be consumed by route-planning, fleet safety, and road-condition prediction systems.

## Section 3: System Architecture

### Textual Flow Diagram

User
-> Frontend UI Layer
-> API Layer
-> ML Verification Engine
-> Database
-> Geospatial Engine (H3)
-> Visualization and Authority Dashboard

### What is implemented

The architecture is layered: React for presentation, FastAPI for request handling and business rules, MongoDB for storage, an image-analysis service for inference, and a clustering service for risk-zone creation.

### How it works

The frontend sends authenticated requests with uploaded images and GPS coordinates. The API validates input, saves images, runs image verification, writes the report and verification record, and optionally updates risk zones through H3 clustering. The authority dashboard then reads the aggregated state for review and repair management.

### Why layered architecture was chosen

Layering separates concerns: UI changes do not rewrite business logic, and ML changes do not force database redesign. It also helps testing because auth, storage, clustering, and inference can each be verified independently.

### Why alternatives were not chosen

A monolith with no separation would be faster to start but harder to test and more fragile as the system grew. A microservices architecture was not chosen because it would add deployment overhead, distributed tracing complexity, and more network failure modes without a clear functional benefit for this project size.

### Trade-off summary

This is a modular monolith style backend with a separate frontend. That choice is simpler to operate than distributed services, but still disciplined enough to keep the major subsystems isolated.

## Section 4: End-to-End Data Flow

### What is implemented

The current pipeline is:
1. User authenticates.
2. User uploads image, description, and coordinates.
3. Frontend packages the data as multipart form data.
4. Backend validates the file and coordinates.
5. Image is saved to disk.
6. Computer vision verification computes confidence.
7. Report and verification records are written to MongoDB.
8. Verified reports feed H3 clustering.
9. Authority dashboard reads aggregated reports and zones.

### How it transforms data

The uploaded image starts as a browser file object and becomes a validated disk artifact. The geolocation starts as client-side coordinates and becomes a bounded location model. The model output starts as feature-derived scores and becomes a normalized verification decision. The stored report becomes a queryable object with report status, AI confidence, H3 index, and audit history.

### Why this flow was chosen

This ordering minimizes wasted work. The system validates and stores only what it can trust, and it uses AI before human review so that authorities see prioritized content instead of raw noise.

### Why alternatives were not chosen

Pushing all processing to the client was rejected because it would expose trust boundaries and allow tampering. Performing clustering before verification was rejected because unverified noise would pollute zone analytics. Delaying persistence until human approval would eliminate useful metadata for traceability.

### Formal pipeline

Let the raw submission be $(I, \ell, d)$ where $I$ is the image, $\ell=(lat, lon)$ is the location, and $d$ is the optional description.

The backend computes:

$v = g(I)$ for verification,
$h = H3(\ell)$ for geospatial bucketing,
and stores

$r = \{I, \ell, d, v, h\}$

with status updates conditioned on $v$.

## Section 5: Technology Stack

### Frontend: React

What it is: A component-based UI library used here with React Router, context providers, and Axios.

Why used here: It supports authenticated multi-page workflows for citizens and authorities without page reloads. The codebase uses it for routing, theme state, auth state, and form handling.

Real-world usage: Responsive dashboards, report forms, and review screens benefit from React because stateful UI and conditional rendering are central to the workflow.

Why not alternatives: A server-rendered-only UI would be less flexible for this interaction-heavy workflow. Angular would also work, but React is lighter for incremental composition and integrates cleanly with the existing codebase.

### Backend: FastAPI

What it is: An async Python web framework used for the API layer.

Why used here: The backend needs request validation, upload handling, JWT auth, and async MongoDB access. FastAPI fits this combination well and generates strong schema-based contracts.

Real-world usage: FastAPI is appropriate when the system combines web APIs, image uploads, and data services.

Why not Node.js / Django: Node.js would be viable, but the existing machine-vision and geospatial stack is Python-native. Django would be heavier than necessary for this API-first design and would add framework weight without improving the core workflow.

### Database: MongoDB

What it is: A document database used for users, pothole reports, verification history, risk zones, and repairs.

Why used here: Report schemas are flexible, image verification is document-shaped, and geospatial clustering benefits from denormalized access patterns. MongoDB indexes support the current query style.

Real-world usage: MongoDB is practical for event-like records, evolving metadata, and operational dashboards.

Why not PostgreSQL: PostgreSQL would be stronger for rigid relational reporting, but this project values flexible document storage and rapid schema evolution for image-driven metadata. A spatial PostGIS design could be strong for GIS-heavy deployments, but the current implementation is already aligned to MongoDB plus H3.

### ML / Vision: OpenCV-based verification, with YOLO tooling in the repository

What it is: The live API uses OpenCV feature extraction and heuristic scoring; repository scripts also include YOLO training and evaluation utilities.

Why used here: The current dataset and deployment requirements favor a light-weight inference path. OpenCV provides deterministic behavior, low runtime overhead, and no model-loading dependency for the primary API flow.

Real-world usage: This is suitable for a first-stage filter or prototype verifier where explainability and operational simplicity matter.

Why not TensorFlow / PyTorch as the live path: Deep models are useful, but they require a trained artifact, more compute, and stronger dataset governance. For this codebase, the operational path is intentionally simpler, while YOLO scripts preserve a route toward more advanced model training.

### Geospatial: H3 hex grid

What it is: Uber H3 is a hierarchical hexagonal indexing system used to bucket pothole reports into risk zones.

Why used here: It groups nearby defects consistently and supports city-scale clustering without directional bias from square grids.

Real-world usage: H3 is widely used in fleet analytics, demand mapping, and location clustering.

Why not square grids or ad hoc radius checks: Square grids introduce directional artifacts, while radius-only grouping is unstable for dense urban layouts. H3 gives a compact, repeatable cell identity and a better clustering primitive.

### Deployment: Vercel and alternatives

What it is: Vercel is a valid frontend deployment target for static React builds.

Why used here: It is a reasonable choice for serving the frontend if the project is split into a browser client and an API backend.

Why not only Vercel: The backend is not a static app; it needs runtime services, MongoDB, and file storage. This project is more realistically deployed with separate frontend hosting plus an API host, or via local Docker-based infrastructure during development.

## Section 6: Machine Learning System

### CNN

### What is implemented

The repository is centered on image-based pothole verification rather than a fully trained convolutional network in the live API path.

### How it works

In a CNN, convolution filters learn feature maps that capture edges, corners, cracks, and texture transitions. Early layers learn local patterns; deeper layers combine them into higher-level road-damage features. Mathematically, a convolution feature map is:

$$
(X * K)(i,j) = \sum_{m}\sum_{n} X(i+m,j+n)K(m,n)
$$

Edge detection emerges because the learned kernels respond strongly to sharp intensity transitions. That is exactly the kind of visual signal potholes create around broken asphalt boundaries.

### Why this approach was chosen

CNNs are the natural model class for image classification because they exploit spatial locality and translation tolerance.

### Why alternatives were not chosen

Hand-engineered features alone are brittle when lighting, shadows, and road texture vary. Pure fully connected models ignore image structure and are inefficient. CNNs therefore remain the most principled choice if the system is trained as a supervised classifier.

### Transfer Learning

### What is implemented

The codebase includes YOLO-related scripts, which indicates a path toward transfer-learned detectors, but the current live endpoint is not dependent on a large pretrained backbone.

### How it works

Transfer learning starts from pretrained weights such as ResNet or MobileNet. Early layers already encode low-level vision primitives, so the model only needs to adapt to road-surface patterns and pothole appearances. This is mathematically justified because image feature hierarchies are reusable across domains.

### Why this approach was chosen

Dataset size is usually the limiting factor in pothole detection. Transfer learning reduces the sample complexity by reusing generic visual features.

### Why alternatives were not chosen

Training a deep model from scratch is data-hungry and unstable for small infrastructure datasets. The current system therefore keeps the live API simple while preserving a path for stronger learned models later.

### YOLO

### What is implemented

The repository contains YOLO training and evaluation scripts, making object detection an available optional route.

### How it works

YOLO predicts bounding boxes and class probabilities in one pass. For pothole detection, that means the model can localize damaged pavement and estimate confidence in real time.

### Why this approach was chosen

YOLO is useful when the product requirement shifts from binary verification to object localization with low latency.

### Why alternatives were not chosen

For the current API, box-level localization is not required for every report. The deployed path therefore prioritizes simpler verification and persistence rather than a heavier real-time detector.

## Section 7: Pothole Detection Decision Logic

### What is implemented

The current verifier combines multiple heuristics:
1. Dark-region detection.
2. Irregular edge detection.
3. Texture discontinuity analysis.
4. Contrast consistency.
5. Hole-like region scoring.

### How it works

The image is converted to grayscale. Each cue generates a sub-score between 0 and 100. The final confidence is a weighted sum, capped at 100. If the score exceeds the minimum confidence threshold, the image is treated as a pothole candidate.

### Why this approach was chosen

This logic is explainable. Under viva scrutiny, every score can be justified by an observable image property rather than an opaque latent vector. That is valuable when the system must be defended to non-ML stakeholders.

### Why alternatives were not chosen

An opaque score-only model would be harder to defend without a labeled dataset and calibration evidence. Pure thresholding on one cue, such as darkness alone, would fail under shadows, wet pavement, or overexposure. The multi-cue design reduces single-point failure.

### Failure cases

Low-light scenes can be mistaken for potholes because darkness is overloaded as a feature. Road patches or manhole covers can look like damage. Strong shadows can mimic crater boundaries. Motion blur suppresses edge evidence and can under-score real potholes.

## Section 8: Model Evaluation Metrics

### What is implemented

The system should be judged using binary classification metrics, not accuracy alone.

### How it works

From the confusion matrix:

Precision $= \frac{TP}{TP+FP}$

Recall $= \frac{TP}{TP+FN}$

F1 $= 2\cdot\frac{Precision \cdot Recall}{Precision + Recall}$

Specificity $= \frac{TN}{TN+FP}$

Accuracy $= \frac{TP+TN}{TP+TN+FP+FN}$

### Why this approach was chosen

Accuracy alone is misleading in imbalanced settings. If most submissions are negative or ambiguous, a model can appear strong while missing real potholes. Precision and recall expose the true behavior of the detector.

### Why alternatives were not chosen

Only using accuracy would hide operational risk. AUC is useful for ranking quality, but it does not directly explain the cost of missed potholes versus false alarms. F1 is more actionable for this workflow because it balances missed detections and unnecessary alerts.

### Trade-off interpretation

If recall is raised aggressively, the system catches more true potholes but may flood authorities with false positives. If precision is prioritized too heavily, the system becomes conservative and misses defects. This project should bias toward higher recall at the first screening stage.

## Section 9: Hexagonal Map System

### What is implemented

Each verified report receives an H3 cell index at resolution 9, and risk zones are aggregated by cell.

### How it works

The geographic coordinate $(lat, lon)$ is converted to a hex cell. Reports in the same or adjacent operational area cluster into a risk zone, and the cluster count determines the risk level.

### Why hex grids beat square grids

Hex grids have more uniform neighbor relationships and less axis bias. Every cell has a more balanced local neighborhood than a square grid, which helps cluster road defects without artifacts caused by horizontal or vertical alignment.

### Why this approach was chosen

Road maintenance decisions are spatial, not only per-image. H3 gives a robust city-scale abstraction for problem concentration.

### Why alternatives were not chosen

Pure latitude-longitude bounding boxes are too crude. Square tiles are easier to implement but create directional bias. H3 is a better balance of mathematical regularity and operational interpretability.

### Uber H3 example

Uber uses H3 for spatial aggregation and operational analytics. In this project, the same principle turns raw pothole points into dense regions that an authority can prioritize.

## Section 10: Database Design and Integrity

### What is implemented

The actual persistence model consists of these collections:
1. Users.
2. Pothole reports.
3. Image verification history.
4. Risk zones.
5. Repair actions.

Images themselves are stored on disk, while image metadata and verification outcomes are stored in MongoDB documents.

### How it works

Users store identity and role. Reports store the user reference, image path, location, H3 index, status, and timestamp. Verification records store report association, confidence score, and detection result. Risk zones store aggregated pothole counts and location centers. Repair actions store zone linkage and workflow state.

### Why this design was chosen

This model is normalized enough to avoid duplication of user identity and repair workflow, but denormalized enough to make dashboard reads fast. Reports and verification history remain separate so that ML evidence is preserved independently from the report lifecycle.

### Why alternatives were not chosen

A fully embedded single-document design would make reports bloated and harder to query over time. Excessive normalization would complicate reads and force multi-collection joins for basic dashboard pages.

### Integrity constraints

User email is unique. Report status is constrained to pending, verified, or rejected. Risk level is constrained to low, medium, or high. Repair status is constrained to pending, in_progress, or completed. These constraints make invalid workflow states harder to persist.

### ACID discussion

MongoDB supports atomicity at the document level. That is sufficient for many report writes, but the risk-zone recalculation flow is not a single multi-document transaction in the current design. That means the delete-and-reinsert clustering update can temporarily expose a replacement window.

## Section 11: Authentication System

### What is implemented

The system uses password-based registration, JWT access tokens, JWT refresh tokens, and role-based authorization.

### How it works

Passwords are hashed before storage. On login, the password is verified and a JWT payload containing user id, email, and role is signed. Protected endpoints decode the bearer token and enforce role checks when authority access is required.

### Why hashing algorithms matter

Hashing protects stored credentials if the database is compromised. The preferred scheme in the codebase is bcrypt through Passlib. A legacy SHA-256 fallback exists for environments where bcrypt initialization fails.

### Why this approach was chosen

JWTs keep the API stateless and convenient for a browser client. Role-based claims are sufficient for the user and authority separation in this project.

### Why alternatives were not chosen

Server sessions would work, but they would require more server-side session state management. OAuth was unnecessary because the system does not currently integrate external identity providers. A pure API-key model would be too coarse for end-user workflows.

### Security note

The SHA-256 fallback is not ideal for production because it is weaker than a modern adaptive password hash. It exists as a compatibility safeguard, not as a preferred production posture.

## Section 12: Performance Model

### What is implemented

The system is optimized for moderate request volume through database indexes, asynchronous I/O, and disk-based file storage.

### How it works

The dominant costs are image upload, image decoding, verification, database writes, and aggregation. MongoDB indexes are created on user email, report status, user id, H3 index, location coordinates, risk zone H3 index, and repair workflow fields to accelerate common queries.

### Bottlenecks

1. Image reading and OpenCV processing are CPU-bound.
2. File I/O grows with image size.
3. Risk-zone recalculation is expensive because it scans verified reports and rebuilds clusters.
4. Dashboard queries can slow down if indexes are missing or if report volume grows sharply.

### Why this approach was chosen

Indexing and async database access deliver the most immediate performance gains for the current scale. The system avoids premature distributed complexity.

### Why alternatives were not chosen

A GPU inference server or full streaming pipeline would be overkill until the data volume and detection model justify it. The present architecture is easier to operate and debug.

### Performance equation

For a request, total latency can be approximated as:

$T_{total} = T_{upload} + T_{validate} + T_{infer} + T_{db} + T_{response}$

The main optimization levers are reducing $T_{infer}$ and $T_{db}$ through lighter models and better indexing.

## Section 13: Testing and Validation

### What is implemented

The repository includes unit, integration, geospatial, database, API, performance, and frontend E2E tests.

### How it works

Auth tests validate login and access control. ML tests exercise the verification logic under normal and extreme image conditions. Database tests validate MongoDB interactions and H3 storage behavior. Integration tests check request flow through the API. Frontend tests validate reporting and dashboard workflows.

### What failed and why

The recent QA history showed failures caused by stale expectations rather than core logic defects: old tests referenced outdated endpoint paths, some assumptions about response shapes no longer matched the live routes, and one frontend workflow test expected an older title string. These were test maintenance problems, not evidence that the live workflow was broken.

### Validation outcome

The later verification pass reported the backend suite as passing and the targeted frontend E2E checks as passing. That matters because it shows the current implementation can be exercised end to end after the stale expectations are corrected.

### Why this approach was chosen

The system needs more than unit tests because pothole reporting spans auth, uploads, ML, geospatial logic, and persistence. End-to-end and integration tests are therefore necessary to defend the workflow as a system, not as isolated functions.

### Why alternatives were not chosen

Pure unit testing would miss route integration failures, auth mismatches, and query path regressions. Pure manual testing would be too weak for a defense-ready technical posture.

## Section 14: Failure and Edge Case Analysis

### Low light

Low light increases false positives because dark asphalt and true potholes become visually similar. The heuristic verifier partially compensates using multiple cues, but darkness remains an unavoidable confounder.

### Blur

Motion blur weakens edge and texture signals, reducing confidence in real potholes. The system may under-detect damaged pavement when the camera is moving quickly.

### False positives

Shadows, puddles, road patches, and manhole covers can look like potholes. This matters because the system is designed to prioritize reporting, not to claim perfect semantic understanding of every road surface irregularity.

### Concurrency issues

The risk-zone recalculation process currently deletes all risk zones and reinserts them. Under concurrent reads, a consumer can briefly observe an empty or partially rebuilt zone set. This is a known consistency risk and should be addressed with a transactional or versioned swap strategy.

### Geolocation failures

If browser geolocation is unavailable or denied, the frontend falls back to default coordinates. That keeps the workflow usable but decreases spatial precision.

## Section 15: Security Analysis

### Injection attacks

The API uses typed request models, ObjectId validation, and bounded fields to reduce malformed input risk. MongoDB query construction is limited and driven by validated parameters, lowering exposure to trivial injection-style abuse.

### Unauthorized access

JWT bearer authentication and role checks protect user and authority endpoints. Regular users are restricted to their own reports, while authority actions require elevated privileges.

### Data leakage risks

Uploaded images are served from a dedicated uploads path, so access control and deployment configuration matter. The frontend also stores tokens locally, which is convenient but increases exposure if the browser environment is compromised.

### Why security matters here

This project handles location data, identity, and potentially sensitive roadway imagery. Even though it is not a financial system, the operational and privacy implications are real.

### Why alternatives were not chosen

Anonymous submission would weaken accountability and make report abuse harder to control. Overly permissive public read access would expose user-linked operational data without a clear need.

## Section 16: Limitations

### ML limitations

The current live verification path is heuristic and therefore less robust than a fully trained deep model under severe environmental variation. It is explainable, but not a substitute for a large, well-labeled dataset.

### Scalability limitations

MongoDB plus file storage is enough for this project scale, but high-volume national deployment would need stronger object storage, better observability, and a more explicit job queue for image processing and clustering.

### Environmental dependency

The system depends on image quality, lighting, and camera angle. It also depends on browser geolocation for location precision and on stable connectivity for uploads.

### Architectural limitations

The current risk-zone recomputation strategy is not transactional across the full collection replacement. That is acceptable for a project-scale system, but not ideal for high-concurrency production use.

## Section 17: Future Improvements

### Real-time detection

Move from upload-only verification toward live camera or dashcam inference with streaming or near-real-time batching.

### Mobile apps

Add mobile capture and offline-first report buffering so citizens can submit incidents from the field with weaker connectivity.

### Advanced ML models

Replace the heuristic verifier with a calibrated CNN or a transfer-learned detector, and use YOLO when bounding-box localization is required.

### Operational improvements

Add versioned risk-zone recomputation, stronger audit logging, storage object lifecycle management, and queue-based inference if submission volume grows.

### Why these are the right next steps

They improve the two core project risks: model robustness and operational scale. The current design is a credible base, but it is intentionally not the final form of a city-wide production platform.

## Section 18: Conclusion

This project is technically strong because it combines authenticated reporting, image verification, H3-based clustering, and authority workflow management into one coherent pipeline. It is real-world ready at the prototype and pilot level because the major operational concerns - capture, verification, persistence, prioritization, and review - are all represented in the architecture.

Its main strength is that it does not stop at detection. It connects detection to location intelligence and maintenance workflow. Its main limitation is that the live verifier is still a lightweight computer-vision system rather than a fully trained deep detector. That limitation is explicit, defensible, and actionable.

The result is a system that can be defended academically and practically: it has mathematical grounding, a clear architecture, measurable trade-offs, known failure modes, and a realistic path to stronger future versions.