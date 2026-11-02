
# GitHub for OpenBIM
## From Sharing Files to Collaborative Workflows

**A3: Teach — Peer-to-Peer Tutorial**

**Audience:** Architecture, Engineering and Construction (AEC) / OpenBIM students  
**Level:** Beginner  
**Format:** Video tutorial with written documentation

---

## About This Tutorial

GitHub is widely used in software development, but its applications extend far beyond programming.

It provides a platform for sharing files, documenting projects, tracking changes, and collaborating with others.

In the context of OpenBIM, GitHub can support the development of open-source tools, the sharing of technical knowledge, and collaboration across different disciplines.

### Central Question

**How can GitHub help AEC students collaborate, document, and share knowledge in an OpenBIM environment?**

### Learning Objectives

After completing this tutorial, students should be able to:

1. Understand what GitHub is and how it works.
2. Navigate GitHub repositories and identify their main components.
3. Understand how GitHub supports collaboration and version control.
4. Recognize the relevance of GitHub to OpenBIM.
5. Identify ways to use GitHub in university and professional projects.

---

## Video Tutorial

Our video introduces GitHub, demonstrates its essential features, and explores its applications in OpenBIM.

**Watch our tutorial here:**

[Video Tutorial — Link coming soon](#)

### Video Overview

| Section | Topic | Duration |
|---|---|---|
| 1 | What is GitHub? | 2 min |
| 2 | How does GitHub work? | 3 min |
| 3 | How can we collaborate? | 3 min |
| 4 | Why is GitHub relevant to OpenBIM? | 3 min |
| 5 | How can we use GitHub ourselves? | 3 min |
| 6 | Summary | 1 min |

The following sections provide additional explanations and references to accompany the video.

---

# 1. What is GitHub?

## 1.1 What is GitHub, and what is it used for?

[GitHub](https://github.com/) is a web-based platform that allows users to store, manage, share, and collaborate on projects.

It is primarily used for software development but can also support:

- Project documentation
- File sharing
- Version control
- Team collaboration
- Open-source development
- Knowledge sharing
- Issue and task management

GitHub makes it possible for individuals and teams to work on shared projects while keeping track of changes.

**Example in AEC:**

An engineering team could use GitHub to share a Python script that checks IFC model properties. Other users could download the script, report problems, and suggest improvements.

## 1.2 What is the difference between Git and GitHub?

Although Git and GitHub are closely connected, they are not the same.

### Git

Git is a version-control system that records changes to files over time.

It allows users to:

- Track modifications
- Compare different versions
- Restore previous versions
- Work on separate branches
- Combine contributions

### GitHub

GitHub is an online platform that hosts Git repositories and provides additional collaboration features.

These include:

- Sharing repositories
- Reviewing changes
- Managing Issues
- Creating Pull Requests
- Organizing project documentation

**In simple terms:**

Git is the technology that tracks changes.

GitHub is the platform where Git-based projects can be shared and collaboratively managed.

## 1.3 What is a repository?

A repository, often called a "repo", is the central location where a project's files and version history are stored.

A repository may contain:

- Source code
- Documentation
- Images
- Configuration files
- Scripts
- Example datasets
- README files

Example structure:

```text
OpenBIM-Project/
|
|-- README.md
|-- documentation/
|-- scripts/
|-- examples/
|-- LICENSE
```

Repositories can be public or private.

**Public repositories** are visible to everyone.

**Private repositories** are accessible only to authorized users.

## 1.4 What does Open Source mean?

Open source generally refers to software whose source code is made available under a license that allows others to use, study, modify, and redistribute it under specified conditions.

Important principles include:

- Transparency
- Collaboration
- Knowledge sharing
- Community-driven improvement
- Reusability

However, a public GitHub repository is not automatically open source.

A suitable license is required to grant reuse and modification rights.

Common open-source licenses include MIT, Apache-2.0, and GPL.

## 1.5 Why is GitHub relevant beyond software development?

GitHub is useful whenever projects require documentation, collaboration, and transparent change tracking.

Examples include:

- Research projects
- University assignments
- Technical documentation
- Data analysis
- Automation workflows
- Educational resources
- Open standards development

Its main advantage is that project information and changes can be organized in one accessible location.

## 1.6 Why should architects, engineers, and BIM managers know about GitHub?

Digital construction increasingly relies on software, automation, open standards, and data exchange.

GitHub provides access to many tools and resources relevant to these activities.

AEC professionals can use GitHub to:

- Discover open-source BIM tools
- Access automation scripts
- Understand software development
- Follow updates to technical projects
- Report bugs and suggest improvements
- Share technical documentation

Programming knowledge is not necessary to browse repositories or access documentation.

### Key Takeaway

**GitHub is more than a platform for programmers. It is an environment for sharing, documenting, and improving technical knowledge.**

---

# 2. How Does GitHub Work?

## 2.1 How do you create a GitHub account?

To create a GitHub account:

1. Visit https://github.com
2. Select "Sign up".
3. Enter the required registration information.
4. Choose a username.
5. Complete the verification process.
6. Configure your profile and security settings.

Two-factor authentication is recommended to protect your account.

Most public repositories can be viewed without an account.

However, an account is generally required to create repositories or contribute to projects.

## 2.2 How do you search for and explore existing projects?

GitHub provides a search function for discovering repositories, code, and other resources.

For example, searching for:

- OpenBIM
- IFC
- IfcOpenShell
- buildingSMART
- BIM automation

can lead to relevant projects.

When opening a repository, several elements are important:

**README**

Explains the purpose of the project and how to use it.

**Code**

Contains the repository's files and folders.

**Issues**

Shows reported problems, questions, and improvement suggestions.

**Pull Requests**

Shows proposed changes and discussions about them.

**Releases**

Provides published versions of a project, when available.

**License**

Explains the legal conditions for using and modifying the project.

**Example:**

The IfcOpenShell repository contains resources related to working with IFC files.

https://github.com/IfcOpenShell/IfcOpenShell

## 2.3 How do you create a repository?

A repository can be created directly through the GitHub website.

The general process is:

1. Log in to GitHub.
2. Select "New repository".
3. Enter a repository name.
4. Add a description.
5. Choose public or private visibility.
6. Optionally initialize it with a README.
7. Select "Create repository".

The repository becomes the central location for the project's files and documentation.

## 2.4 How do you upload and organize files?

Files can be uploaded directly through GitHub's web interface.

In a repository, select:

**Add file → Upload files**

After selecting the files, GitHub allows users to enter a commit message describing the change.

Files can be organized into folders to make the project easier to understand.

For example:

```text
BIM-Documentation/
|
|-- README.md
|-- tutorials/
|-- images/
|-- scripts/
|-- references/
```

A clear folder structure improves accessibility and makes collaboration easier.

Sensitive information, passwords, and confidential project files should not be uploaded without appropriate authorization.

## 2.5 What are commits, and how does version control work?

A commit records a set of changes made to a repository.

Each commit usually includes:

- The changes made
- The author
- The date
- A descriptive message

For example:

"Updated IFC documentation"

Version control allows users to compare changes and access previous versions.

Instead of creating multiple files such as:

```text
project_final_v1
project_final_v2
project_final_v3
```

Git can track changes within the same file.

This improves transparency and reduces confusion.

## 2.6 What is a README file, and why is it important?

A README is usually the first document visitors see when opening a GitHub repository.

It is commonly named:

`README.md`

The `.md` extension stands for Markdown, a lightweight language used to format text.

A README can include:

- Project descriptions
- Instructions
- Images
- Links
- Tables
- Examples
- Technical documentation

A well-written README helps users understand what a project does and how they can use it.

**This document is itself an example of a GitHub README.**

### Key Takeaway

**Repositories organize projects, commits track changes, and README files make information understandable and accessible.**

---

# 3. How Can We Collaborate Using GitHub?

## 3.1 How can multiple people contribute to the same project?

GitHub allows several people to collaborate on shared repositories.

Depending on their permissions, contributors can:

- Add or edit files
- Suggest improvements
- Report problems
- Review changes
- Discuss new features

Project owners can invite collaborators and manage their access rights.

For public open-source projects, external contributors can often propose changes through forks and pull requests.

A typical collaboration process is:

**Issue → Branch → Change → Commit → Pull Request → Review → Merge**

This provides a structured approach to teamwork.

## 3.2 What is the difference between public and private repositories?

### Public Repository

A public repository can be viewed by anyone.

It is useful for:

- Open-source projects
- Public documentation
- Educational resources
- Community collaboration

Public visibility does not mean everyone can directly edit the project.

### Private Repository

A private repository is accessible only to authorized users.

It is useful for:

- Internal projects
- University group work
- Confidential documentation
- Team development

Access permissions can be managed by repository owners.

## 3.3 What are branches and pull requests?

### Branches

A branch is a separate line of development within a repository.

It allows contributors to work on changes without immediately affecting the main version.

For example:

A team member could create a branch to improve the documentation of an IFC workflow.

### Pull Requests

A pull request proposes that changes from one branch should be integrated into another.

Other contributors can:

- Review the changes
- Leave comments
- Suggest improvements
- Approve or request revisions

Once accepted, the changes can be merged.

This process supports quality control and collaboration.

## 3.4 How can GitHub Issues be used to track tasks and problems?

GitHub Issues are used to document and discuss tasks, problems, questions, and improvement suggestions.

An Issue may contain:

- A title
- A description
- Screenshots
- Labels
- Assigned contributors
- Discussion comments

**Example in OpenBIM:**

A user discovers that a script does not correctly recognize an IFC property set.

They create an Issue explaining the problem.

Other contributors can investigate and discuss possible solutions.

Issues therefore support communication and continuous improvement.

## 3.5 How can we review and track changes made by others?

GitHub provides several features for reviewing project history.

**Commit History**

Shows recorded changes over time.

**Pull Request Reviews**

Allow users to inspect proposed changes and provide feedback.

**Files Changed**

Highlights additions and deletions in text-based files.

**Blame View**

Shows which commit last changed a particular line of a file.

These tools make project development more transparent.

## 3.6 How can GitHub improve transparency and accountability?

GitHub documents many aspects of collaboration.

For example:

- Who submitted a change?
- When was it submitted?
- What was modified?
- Why was the change proposed?
- Was the change reviewed?

This information can support communication, documentation, and project handovers.

However, GitHub activity does not necessarily reflect the total amount or quality of work contributed by a person.

### Key Takeaway

**GitHub supports collaboration not only by sharing files but also by documenting decisions, changes, and discussions.**

---

# 4. Why Is GitHub Relevant to OpenBIM?

## 4.1 What role does GitHub play in the OpenBIM ecosystem?

OpenBIM promotes interoperability, open standards, and collaboration across different software applications and disciplines.

GitHub supports these principles by providing an environment where technical resources can be shared and developed collaboratively.

GitHub can host:

- Open-source BIM software
- IFC-related libraries
- Automation scripts
- Technical documentation
- Example workflows
- Supporting resources for open standards

However, GitHub is not itself an OpenBIM standard or a dedicated BIM model management platform.

## 4.2 Which OpenBIM tools and projects are available on GitHub?

Several relevant organizations and projects use GitHub.

### Example 1: IfcOpenShell

https://github.com/IfcOpenShell/IfcOpenShell

IfcOpenShell is an open-source project providing tools and libraries for working with IFC data.

It supports workflows involving:

- IFC file processing
- Data extraction
- Model analysis
- BIM automation
- Open-source BIM software development

Its GitHub repository demonstrates how developers collaborate on technical BIM tools.

### Example 2: buildingSMART International

https://github.com/buildingSMART

buildingSMART International develops and maintains open standards for the built asset industry.

Its GitHub organization contains repositories related to standards, specifications, and supporting technical resources.

This demonstrates how GitHub can contribute to transparent technical development.

Formal standardization decisions still follow the organization's established governance processes.

### Example 3: Speckle

https://github.com/specklesystems

Speckle provides technologies for sharing and working with AEC data.

Its GitHub organization contains open-source components related to its ecosystem.

This example highlights the distinction between GitHub as a software development platform and specialized tools for working with AEC data.

## 4.3 How can GitHub be used to share BIM scripts, documentation, and workflows?

GitHub can provide a central location for sharing reusable BIM-related resources.

For example, a team could publish:

- Python scripts for IFC analysis
- Instructions for model checking
- Workflow diagrams
- Technical documentation
- Example datasets
- Automation templates

A repository could be organized as follows:

```text
IFC-Quality-Checking/
|
|-- README.md
|-- scripts/
|   |-- check_properties.py
|
|-- documentation/
|   |-- workflow.md
|
|-- examples/
|   |-- example_report.csv
```

Other users could access the documentation, understand the workflow, and suggest improvements.

## 4.4 How does GitHub support the development of open standards?

Open standards benefit from transparent documentation and collaborative technical development.

GitHub can help organizations:

- Publish technical resources
- Track proposed modifications
- Discuss improvements
- Document development history
- Collect community feedback

For example, technical resources associated with buildingSMART standards can be explored through GitHub.

However, publishing or merging changes on GitHub does not automatically mean a standard has been formally approved.

## 4.5 What are the benefits and limitations of GitHub for BIM projects?

### Benefits

**Transparency**

Changes and discussions can be documented.

**Collaboration**

Multiple contributors can participate in development.

**Accessibility**

Public repositories allow knowledge and tools to be shared widely.

**Version Control**

Previous versions of text-based files and scripts can be tracked.

**Knowledge Sharing**

Documentation and examples can be made available to the community.

### Limitations

**Large BIM Files**

Large IFC and native BIM model files are often unsuitable for ordinary Git version-control workflows.

**Model Coordination**

GitHub does not replace specialized BIM collaboration platforms or Common Data Environments (CDEs).

**Technical Complexity**

Some advanced Git workflows require additional knowledge.

**Data Security**

Public repositories may expose sensitive project information.

**Quality Assurance**

Not every public repository is actively maintained or suitable for professional use.

### GitHub vs. Common Data Environment (CDE)

| GitHub | CDE |
|---|---|
| Code and script management | Project information management |
| Documentation | BIM model coordination |
| Version control for text-based files | Managed model and document workflows |
| Open-source collaboration | Project delivery and approvals |
| Issue tracking | Formal information exchange |

GitHub and CDE platforms can complement one another, but they serve different purposes.

### Key Takeaway

**GitHub supports the development and sharing of OpenBIM knowledge and tools, while specialized BIM platforms remain important for model-based collaboration.**

---

# 5. How Can We Use GitHub Ourselves?

## 5.1 How can we create a shared project?

A shared GitHub repository can provide a central location for group documentation, scripts, and other resources.

A typical process includes:

1. Creating a repository.
2. Defining its purpose.
3. Adding a README.
4. Organizing folders.
5. Inviting collaborators.
6. Managing access permissions.

For example, a university group could create an `OpenBIM-Learning-Resources` repository.

It could contain useful links, explanations, tutorials, and examples.

## 5.2 How do we upload and edit files?

GitHub provides a browser-based interface for basic file management.

### Uploading Files

Open a repository and select:

**Add file → Upload files**

Select the files and confirm the change with a commit message.

### Editing Files

Open a text file, select the edit option, modify its contents, and commit the changes.

For users without direct write access, GitHub may offer a fork-and-pull-request workflow.

This means that basic editing and documentation can be performed without installing additional software.

## 5.3 How can we document our work using a README?

A README should explain the project's purpose and provide the information required to understand and use it.

A simple README structure might include:

```text
Project Title

1. Introduction
2. Project Purpose
3. Features
4. Documentation
5. Resources
6. Contributors
7. License
```

Markdown makes it possible to format these sections using headings, links, images, and tables.

A clear README improves communication and makes projects easier to reuse.

## 5.4 How do we contribute to another person's repository?

Contributing to an existing repository usually involves the following process:

1. Explore the repository.
2. Read its README and contribution guidelines.
3. Identify a possible improvement.
4. Check existing Issues and pull requests.
5. Create a fork or branch if appropriate.
6. Make the proposed change.
7. Open a pull request.
8. Wait for review and respond to feedback.

Repository maintainers decide whether a contribution is accepted.

Not every project accepts external contributions.

## 5.5 How can we use GitHub in future university or professional projects?

GitHub can support different types of AEC and OpenBIM projects.

### University Projects

- Organizing group documentation
- Sharing learning resources
- Managing scripts
- Tracking project tasks
- Documenting technical workflows

### Professional Applications

- Developing BIM automation tools
- Managing technical documentation
- Sharing reusable scripts
- Collaborating on open-source projects
- Tracking software issues
- Maintaining reproducible workflows

**Example:**

A BIM team develops a Python script that checks the completeness of IFC properties.

GitHub can be used to store the script, document how it works, track improvements, and coordinate contributions.

The actual project models may remain in a dedicated CDE.

### Key Takeaway

**GitHub can help students and professionals organize knowledge, collaborate on technical resources, and improve workflows over time.**

---

# 6. Summary

GitHub is a platform for hosting repositories and supporting collaboration.

The most important concepts covered in this tutorial are:

| Concept | Meaning |
|---|---|
| Git | Version-control system |
| GitHub | Platform for hosting and collaborating on Git projects |
| Repository | Central location for project files and history |
| README | Main project documentation |
| Commit | Recorded change |
| Branch | Separate line of development |
| Pull Request | Proposal to integrate changes |
| Issue | Task, problem, or improvement suggestion |
| Fork | Personal copy of another repository |
| Open Source | Software distributed under a license granting reuse and modification rights |

## Why Does This Matter for OpenBIM?

OpenBIM is based on principles of interoperability, collaboration, and open standards.

GitHub supports these principles by enabling:

- Open-source development
- Transparent documentation
- Collaborative improvement
- Knowledge exchange
- Access to reusable tools and resources

GitHub is particularly valuable for scripts, technical documentation, and software development.

It complements rather than replaces dedicated BIM collaboration platforms.

---

# 7. Further Reading and Resources

### GitHub Documentation

- [GitHub Official Website](https://github.com/)
- [GitHub Getting Started](https://docs.github.com/en/get-started)
- [About Repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories)
- [About Pull Requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
- [Markdown Documentation](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)

### OpenBIM Resources

- [IfcOpenShell](https://github.com/IfcOpenShell/IfcOpenShell)
- [buildingSMART International](https://github.com/buildingSMART)
- [Speckle](https://github.com/specklesystems)

---

## Final Thoughts

GitHub allows us to move beyond simply sharing finished files.

It provides an environment where knowledge, documentation, and technical resources can be continuously developed and improved.

For AEC students, understanding GitHub is an opportunity to explore open-source technologies and collaborative digital workflows.

**The goal is not to become a software developer, but to understand how GitHub can support collaboration, transparency, and knowledge sharing in OpenBIM.**

---

*Created for A3: Teach — Advanced OpenBIM.*

*Video tutorial and documentation prepared as a peer-learning resource.*


