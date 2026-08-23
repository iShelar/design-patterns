# Design patterns, ranked by importance for Amazon LLD

Not a generic GoF catalog — ranked by how often each pattern actually
shows up (or gets explicitly *rejected*) across `amazon-lld.pdf` and
`roadmap.md`. Each principle in `00-foundations/` is the "why"; each
pattern here is a named, reusable "how."

## Tier 1 — must know cold, come up unprompted in this question set

| Pattern | One-liner | Where it's used here |
|---|---|---|
| **Strategy** | Swap an algorithm/policy at runtime by injecting an object instead of branching on a type/enum. | `01-parking-lot` (spot-assignment policy), `08-file-search` (search-by-size/extension/name), `05-chess` (per-piece move validation), `02-elevator` follow-up (dispatch policy across multiple cars). `00-foundations/02_open_closed.py` is this pattern applied to OCP. |
| **State** | An object's behavior changes with its internal mode; move each mode's behavior into its own class instead of `if self.status == ...` scattered across every method. | `02-elevator` — see `02-elevator/reference/elevator.py` vs. `naive_elevator.py` for the concrete failure mode (duplicated transition logic) this pattern removes. |
| **Observer** | Subscribers register for an event; the publisher notifies all of them instead of every reader re-querying/re-scanning on demand. | `06-movie-booking` (new-show-added updates cinema/movie search lists), `07-food-ordering` (rating-changed updates sorted-by-rating views) — PDF calls both out by name. |
| **Factory** (Simple Factory / Factory Method) | Centralize "which concrete class do I construct" so callers depend on an abstraction, not a constructor list. | `05-chess` — `ChessPieceFactory` builds king/queen/pawn/etc. Pairs with Strategy there (create the piece, then validate its move). |
| **Specification** | Combine boolean predicates (AND/OR/NOT) as composable objects instead of a `search(criteria, mode)` method that hardcodes boolean logic. | `08-file-search` follow-up — PDF explicitly calls this out for combining "size > 2MB AND extension = .jpg" style queries. |

## Tier 2 — very likely to come up as a follow-up or a "have you considered"

| Pattern | One-liner | Where it's relevant here |
|---|---|---|
| **Builder** | Construct a complex object step by step instead of a telescoping constructor with many optional args. | `03-pizza-pricing` — building up a pizza with a variable set of toppings is the classic Builder shape; the PDF's own answer is to *not* reach for Decorator here (see below), and Builder is the more defensible fit if an interviewer pushes for a named pattern at all. |
| **Decorator** | Wrap an object to add behavior/cost layers without subclassing per combination. | `03-pizza-pricing` — the PDF explicitly warns interviewers may expect this and calls it unnecessary complexity for this problem. Knowing *why not* here is the actual signal; see `03-pizza-pricing`'s roadmap entry. |
| **Singleton** | Exactly one instance, globally accessible. | Tempting for things like a single `ParkingLot` or `Elevator` dispatcher registry — know the thread-safety subtlety (double-checked locking / lazy init races) if you reach for it, and be ready to justify why DI (see `00-foundations/05_dependency_inversion.py`) is usually the better answer for testability. |
| **Composite** | Treat individual objects and groups of them through the same interface, recursively. | `11-dsa-flavored` — Design File System (directories containing files/directories is the textbook Composite shape). |

## Tier 3 — good breadth, less likely to be load-bearing in this question set

| Pattern | One-liner |
|---|---|
| **Command** | Encapsulate a request (with its undo) as an object — relevant if `11-dsa-flavored`'s Excel formula question grows an undo requirement. |
| **Template Method** | Fix an algorithm's skeleton in a base class, defer specific steps to subclasses. |
| **Chain of Responsibility** | Pass a request along a chain of handlers until one handles it — a natural fit for `03-pizza-pricing`'s mutual-exclusion *rule* checks if that list grows past a couple of rules. |
| **Adapter / Facade** | Translate one interface to another / hide a subsystem behind a simpler one — general-purpose, not tied to a specific topic here. |

## How to use this list

Don't study patterns standalone. Go topic-by-topic per `roadmap.md`; each
topic's `PROBLEM.md` names which pattern the PDF expects and why. Come
back here when you want the cross-topic view — e.g. noticing that Strategy
alone covers four different topics is itself an interview-useful
observation ("this is the same shape as X").
