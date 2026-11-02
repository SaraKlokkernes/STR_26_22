# GitHub for OpenBIM: From Sharing Files to Collaborative Workflows

> **A3: Teach — Peer-to-peer tutorial**  
> **Audience:** Architecture, Engineering and Construction (AEC) / OpenBIM students  
> **Level:** Beginner  
> **Format:** Guided reading, video

## Why this tutorial?

GitHub is widely used to develop software, but its value extends beyond programming. It provides a place to share documentation, track changes, coordinate tasks and contribute to open-source projects. In an OpenBIM context, this can help students discover useful tools, share scripts and examples, and understand how open standards and software evolve.

**Central question:** *How can GitHub help AEC students collaborate, document and share knowledge in an OpenBIM environment?*

### Learning outcomes

By the end, you should be able to:

1. Explain what GitHub is and distinguish it from Git.
2. Navigate a repository, read its documentation and make a simple change.
3. Describe how teams collaborate with issues, branches, commits and pull requests.
4. Identify useful OpenBIM projects on GitHub and understand the platform's limitations.
5. Apply a basic GitHub workflow to a student project.

### Contents

1. [What is GitHub?](#1-what-is-github)
2. [How does GitHub work?](#2-how-does-github-work)
3. [How can we collaborate using GitHub?](#3-how-can-we-collaborate-using-github)
4. [Why is GitHub relevant to OpenBIM?](#4-why-is-github-relevant-to-openbim)
5. [How can we use GitHub ourselves?](#5-how-can-we-use-github-ourselves)
6. [Hands-on exercise](#6-hands-on-exercise)
7. [Quick reference and further reading](#7-quick-reference-and-further-reading)

---

## 1. What is GitHub?

### 1.1 What is GitHub, and what is it used for?

[GitHub](https://github.com/) is an online platform for hosting Git repositories and coordinating work around them. A repository can contain code, documentation, scripts, configuration files and other project resources. GitHub adds a web interface and collaboration features such as **Issues**, **Pull Requests**, **Discussions** and access controls.

**AEC example:** A project team could publish a Python script that checks IFC properties, explain how to use it in a README, and collect bug reports through Issues.

### 1.2 What is the difference between Git and GitHub?

| Git | GitHub |
| --- | --- |
| A version-control system | A hosting and collaboration platform built around Git |
| Tracks file changes and their history | Hosts repositories online and adds collaboration tools |
| Can work locally without an internet connection | Usually accessed online through a browser or connected tools |
| Does not require a GitHub account | Requires an account for most contribution actions |

**Remember:** Git is the underlying technology; GitHub is one place where Git projects can be hosted and collaboratively managed. GitHub is not the only Git hosting service.

### 1.3 What is a repository?

A **repository** (often called a *repo*) is a project's home. It contains files and, when tracked with Git, a history of changes. A repository might include:

```text
openbim-student-project/
├── README.md             # Project overview and instructions
├── docs/                 # Guides and explanations
├── scripts/              # Small automation scripts
├── examples/             # Sample data (where suitable)
├── .gitignore            # Files Git should not track
└── LICENSE               # Terms for reusing the project
```

A repository can be **public** (visible to everyone) or **private** (limited to authorized people).

### 1.4 What does open source mean?

**Open source** generally means that software's source code is available under a license granting rights to use, study, modify and redistribute it under specified conditions. **Publicly visible does not automatically mean open source**: without a suitable license, reuse rights may be limited.

Common licenses include MIT, Apache-2.0 and GPL licenses. Always check the repository's `LICENSE` file before copying or adapting work. For datasets and documentation, different licenses may apply.

### 1.5 Why is GitHub relevant beyond software development?

GitHub can support many text-based, versioned collaborative activities: technical documentation, research notes, reproducible workflows, templates, issue tracking and learning resources. It is particularly effective when teams need to see **who changed what, when, and why**.

### 1.6 Why should architects, engineers and BIM managers know about GitHub?

AEC teams increasingly encounter open-source BIM tools, scripts, plugins and technical standards. Knowing how to read a README, inspect an Issue and locate a release makes it easier to evaluate and reuse these resources responsibly—even without being a programmer.

**Key takeaway:** GitHub is not just a code website; it is a structured environment for sharing and improving project knowledge.

---

## 2. How does GitHub work?

### 2.1 How do you create a GitHub account?

1. Visit [github.com](https://github.com/) and select **Sign up**.
2. Follow the registration steps and verify your email if requested.
3. Choose a recognizable username and configure your profile.
4. Enable **two-factor authentication** to protect your account.

You can browse most public repositories without an account, but you generally need to sign in to create repositories, Issues or pull requests.

### 2.2 How do you search for and explore existing projects?

Use GitHub's search bar to search by keywords such as `IFC`, `OpenBIM`, `IfcOpenShell` or `buildingSMART`. Open a repository and look at:

- **README:** What is the project, and how do you use it?
- **Files and folders:** What does it contain?
- **Issues:** Which bugs, requests or discussions are open?
- **Pull requests:** What changes are being proposed?
- **Releases:** Are there published versions to download?
- **LICENSE:** What are you allowed to reuse?
- **Recent activity:** Is the project still maintained? (Activity alone does not guarantee quality.)

**Tip:** To download a snapshot of a repository, use **Code → Download ZIP**. This gives you the files but not a working Git history. For an ongoing contribution workflow, use a clone or GitHub's browser editing tools.

### 2.3 How do you create a repository?

1. Sign in and click **+ → New repository** (or visit [github.com/new](https://github.com/new)).
2. Enter a name, for example `openbim-learning-lab`.
3. Add an optional description.
4. Choose **Public** or **Private**.
5. Select **Add a README file**.
6. Click **Create repository**.

**Tip:** Start with a README so others immediately understand the repository's purpose.

### 2.4 How do you upload and organize files?

In your repository, choose **Add file → Upload files**, select the files, enter a short commit message and confirm the change. Organize content into clear folders such as `docs/`, `scripts/` and `examples/`.

Avoid uploading passwords, access tokens, confidential project data or personal information. GitHub is also not an ideal default location for very large, frequently changing BIM model files.

### 2.5 What are commits, and how does version control work?

A **commit** records a set of changes in a repository's history, usually with a message explaining the change. For example:

```text
Add IFC property-checking instructions
```

Version control helps teams review earlier changes, compare versions and understand why a document or script evolved. A commit is **not** the same as uploading a complete new copy of a project with a filename like `final_v7_really_final`.

**Example:** Instead of maintaining `guide_v1.md`, `guide_v2.md` and `guide_final.md`, keep `guide.md` and use commit history to track revisions.

### 2.6 What is a README file, and why is it important?

A `README.md` is the introductory document shown prominently on a repository's main page. The `.md` extension means **Markdown**, a simple formatting language for headings, links, lists, tables and code blocks.

A useful README answers:

- What is this project?
- Who is it for?
- How do I get started?
- How do I use or contribute to it?
- Where can I find examples, documentation and license information?

**Key takeaway:** A clear README makes shared work understandable and reusable.

---

## 3. How can we collaborate using GitHub?

### 3.1 How can multiple people contribute to the same project?

A repository owner can invite collaborators or manage access through an organization. Team members can propose and review changes. For public open-source projects, outside contributors often **fork** a repository (make their own copy), work on a change, and open a pull request to the original project.

A simple collaboration cycle is:

```text
Idea → Issue → Branch → Edit → Commit → Pull Request → Review → Merge
```

Not every project uses every step, but this is a useful beginner workflow.

### 3.2 What is the difference between public and private repositories?

| Public repository | Private repository |
| --- | --- |
| Anyone can view its content | Only authorized users can access its content |
| Useful for open learning resources and open-source projects | Useful for team work that should not be public |
| Visibility does not give everyone permission to edit | Collaborators need appropriate access permissions |

**Important:** Even private repositories require careful handling of confidential data and credentials. Follow your university's or project's data-sharing policies.

### 3.3 What are branches and pull requests?

A **branch** is a separate line of development. It lets you work on a change without immediately modifying the main branch. A **pull request (PR)** asks others to review and potentially merge those changes.

**Example:** A student creates a branch named `improve-ifc-guide`, edits a tutorial and opens a PR. Teammates review the change and, if approved, merge it into `main`.

A pull request is not the same as downloading a file: it is a proposal to integrate changes into a repository.

### 3.4 How can GitHub Issues be used to track tasks and problems?

An **Issue** is a place to describe a task, question, bug or improvement. A good Issue typically includes:

- A descriptive title
- Context or the problem
- Steps to reproduce (for bugs)
- The expected outcome
- Relevant screenshots or links, when appropriate

**AEC example:** `IFC example file is missing the required property set` could be an Issue in a shared validation-script repository.

### 3.5 How can we review and track changes made by others?

Open the **Commits** history to see recorded changes. In a pull request, use **Files changed** to inspect additions and deletions, then leave comments or request revisions. The **Blame** view can help identify the commit that last changed a particular line of a text file.

### 3.6 How can GitHub improve transparency and accountability?

Commit histories, issue discussions and PR reviews provide a traceable record of decisions and contributions. This can make handovers and teamwork clearer. However, a commit history does **not** measure a person's overall effort or guarantee that changes are correct.

**Key takeaway:** Collaboration is more than sharing files; it includes communicating decisions and reviewing changes.

---

## 4. Why is GitHub relevant to OpenBIM?

### 4.1 What role does GitHub play in the OpenBIM ecosystem?

OpenBIM promotes interoperability and open standards across AEC software and workflows. GitHub supports this ecosystem by hosting tools, code, documentation, examples and discussions. It is **not itself an OpenBIM standard or a dedicated BIM model server**.

### 4.2 Which OpenBIM tools and projects are available on GitHub?

Here are three useful starting points:

| Project / organization | GitHub link | What to explore |
| --- | --- | --- |
| **IfcOpenShell** | [IfcOpenShell/IfcOpenShell](https://github.com/IfcOpenShell/IfcOpenShell) | Open-source tools and libraries for IFC workflows; README, issues and source code |
| **buildingSMART International** | [buildingSMART](https://github.com/buildingSMART) | Repositories related to open BIM standards, specifications and supporting resources |
| **Speckle** | [specklesystems](https://github.com/specklesystems) | Open-source components of an AEC data collaboration ecosystem |

**Suggested live demo:** Open one of these repositories, locate its README, inspect an Issue, and identify the license and any release information.

### 4.3 How can GitHub be used to share BIM scripts, documentation and workflows?

A team can publish a script for checking IFC properties alongside instructions, sample input/output and known limitations. Other users can propose fixes or request features. For example:

```text
ifc-quality-check/
├── README.md
├── scripts/
│   └── check_properties.py
├── docs/
│   └── workflow.md
└── examples/
    └── sample-report.csv
```

Include the software versions and dependencies required to reproduce results. Share model data only when you have permission to do so.

### 4.4 How does GitHub support the development of open standards?

Organizations can publish technical specifications and supporting resources, discuss proposed changes, and track revisions publicly. Some buildingSMART work is accessible through GitHub. However, **formal standardization and approval happen through the relevant standards organization's governance processes**, not simply because a pull request was merged.

### 4.5 What are the benefits and limitations of using GitHub for BIM projects?

**Benefits**

- Transparent history for text-based documentation and scripts
- Easier collaboration and peer review
- Access to open-source tools and learning resources
- Public issue tracking and knowledge sharing
- Reusable project templates and examples

**Limitations**

- Large binary IFC or native authoring files are less suitable for ordinary Git diff/merge workflows.
- GitHub does not provide all the model coordination, permissions, approval workflows and visualization functions of a specialized Common Data Environment (CDE).
- Public repositories can expose sensitive project information if files are shared carelessly.
- A public repository may be outdated, unlicensed or unmaintained; always evaluate before use.

**Practical distinction:** Use GitHub primarily for **scripts, configuration, documentation, issues and manageable examples**. Use an appropriate CDE or BIM collaboration platform for **live project models and formal information management**. Git LFS can help store certain large files, but it does not make binary BIM model merging straightforward.

**Key takeaway:** GitHub complements OpenBIM workflows; it does not replace BIM-specific collaboration infrastructure.

---

## 5. How can we use GitHub ourselves?

### 5.1 How can we create a shared project?

One team member creates a repository, adds a README and invites teammates through **Settings → Collaborators and teams** (wording may vary with repository ownership). Agree on a folder structure, naming conventions and a simple workflow before adding content.

**Suggested project:** `openbim-learning-lab`, a shared collection of links, terminology and beginner resources.

### 5.2 How do we upload and edit files?

**Upload:** Open the repository → **Add file → Upload files** → choose files → enter a commit message → confirm.

**Edit in browser:** Open a text file such as `README.md` → select the pencil/edit control → make changes → select **Commit changes**. If you do not have direct write access, GitHub may offer a fork-and-pull-request workflow instead.

For your first exercise, editing Markdown is simpler and more reliable than editing an IFC file.

### 5.3 How can we document our work using a README?

Use a short structure like this:

```markdown
# OpenBIM Learning Lab

## Purpose
A shared resource collection for our OpenBIM class.

## Resources
- [IfcOpenShell](https://github.com/IfcOpenShell/IfcOpenShell)
- [buildingSMART](https://github.com/buildingSMART)

## How to contribute
Open an Issue to suggest a resource, or propose an edit through a pull request.

## Team
Add contributors here with their permission.
```

Keep the document current, use descriptive links and explain what readers should do next.

### 5.4 How do we contribute to another person's repository?

1. Read the project's README and any `CONTRIBUTING.md` instructions.
2. Check existing Issues and pull requests to avoid duplicate work.
3. For a small improvement, use the browser editor; GitHub may prompt you to fork the repository.
4. Create a branch, make your change and commit it with a clear message.
5. Open a pull request describing **what changed** and **why**.
6. Respond to review comments; a maintainer decides whether to merge.

**Remember:** Not every repository accepts outside contributions, and an open PR is not guaranteed to be merged.

### 5.5 How can we use GitHub in future university or professional projects?

Possible applications include maintaining course notes, publishing reproducible analysis scripts, documenting an IFC-checking workflow, collecting open-source BIM resources, tracking tasks and coordinating development of small automation tools.

**Example:** For a group assignment, create a private repository for scripts and documentation, use Issues to assign tasks, and use PRs to review important changes. Keep confidential or large model data in an approved system rather than assuming GitHub is the right place.

**Key takeaway:** Start with a small, useful workflow and expand only when the team needs more advanced features.

---

## 6. Hands-on exercise

### Our first collaborative OpenBIM repository (10–15 minutes)

**Goal:** Every participant should interact with a real repository and make at least one contribution.

**Preparation by the tutorial team:**

- Create a repository called `openbim-learning-lab` with a README and a `docs/` folder.
- Add a starter file `docs/resources.md` containing two or three OpenBIM links.
- Decide whether students will be invited as collaborators or will contribute via forks.
- Make sure everyone has a GitHub account if they will create Issues or PRs.
- Test the exercise in advance with a second account.

**Participant checklist:**

- [ ] **Step 1 — Explore:** Open the repository and locate the README, file list and Issues tab.
- [ ] **Step 2 — Ask:** Create an Issue titled `Suggest an OpenBIM learning resource`. Explain which resource you would add and why.
- [ ] **Step 3 — Edit:** Create a branch (or fork), then add a link and a one-sentence description to `docs/resources.md`.
- [ ] **Step 4 — Commit:** Save your edit with a message such as `Add an IFC learning resource`.
- [ ] **Step 5 — Propose:** Open a pull request, briefly explain your change and request a review.
- [ ] **Step 6 — Reflect:** Review one proposed change together and merge it if appropriate.

**If time is short:** Complete Steps 1–2 with everyone, and demonstrate Steps 3–6 live with one volunteer.

### Check your understanding

1. **Git or GitHub?** Which one is the version-control system?  
   **Answer:** Git. GitHub hosts Git repositories and provides collaboration features.
2. **Why use a pull request?**  
   **Answer:** To propose changes and allow discussion and review before merging.
3. **Can anyone edit a public repository?**  
   **Answer:** No. Anyone can view it, but writing directly requires permission; others may contribute through forks and PRs where permitted.
4. **Should you use GitHub as your main storage for a large live IFC coordination model?**  
   **Answer:** Usually no. A dedicated CDE/BIM platform is typically better suited to model coordination and formal project information management.
5. **What should you check before reusing an open-source BIM script?**  
   **Answer:** Its license, documentation, dependencies, maintenance status, security implications and suitability for your workflow.

### Reflection questions

- What did you find easiest or most confusing?
- What is one GitHub feature you could use in your next group project?
- What would make this tutorial more helpful for beginners?

These responses can support peer feedback and reflection on the teaching process.

---

## 7. Quick reference and further reading

| Term | Meaning |
| --- | --- |
| **Git** | Version-control system for tracking changes |
| **GitHub** | Platform for hosting Git repositories and collaborating |
| **Repository** | Project files and their tracked history |
| **README** | Main introductory project document, often written in Markdown |
| **Commit** | Recorded set of changes with a message |
| **Branch** | Separate line of work within a repository |
| **Pull Request** | Proposal to review and integrate changes |
| **Issue** | Task, bug report, question or improvement request |
| **Fork** | Your own copy of another repository, useful for contributions |
| **Clone** | Local copy of a Git repository with its history |
| **License** | Terms specifying how others may use and redistribute material |
| **CDE** | Common Data Environment used for managed project information workflows |

### Useful links

- [GitHub Docs — Getting started](https://docs.github.com/en/get-started)
- [GitHub Docs — About repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories)
- [GitHub Docs — About pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
- [GitHub Docs — Basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [GitHub Skills — Interactive courses](https://skills.github.com/)
- [IfcOpenShell on GitHub](https://github.com/IfcOpenShell/IfcOpenShell)
- [buildingSMART on GitHub](https://github.com/buildingSMART)
- [Speckle on GitHub](https://github.com/specklesystems)

---

**Final message:** GitHub helps us move from *sharing a finished file* to *collaboratively developing, documenting and improving a project*. In OpenBIM, this is particularly valuable for open-source tools, scripts, technical knowledge and transparent workflows—while dedicated BIM platforms remain important for model-based project delivery.

*Created as a peer-learning resource for A3: Teach. Adapt the exercise, timing and repository permissions to your class.*

