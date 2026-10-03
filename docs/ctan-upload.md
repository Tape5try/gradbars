# CTAN resubmission guide for gradbars 0.0.3

The earlier 0.0.1 submission was held for authorship clarification. A GitHub push
does not update CTAN. Send the clarification as a plain-text English reply to
ctan@ctan.org; upload software through the web form, not as an email attachment.

## Author and maintainer

The author and maintainer is **SuFan (苏凡)**. **Tape5try** is the same
person's GitHub username. Contact: **3546236610@qq.com**.
LICENSE, both READMEs, the package header and both manuals now consistently
identify SuFan. The MIT license terms are unchanged.

## Technical changes already prepared

- English manual source and compiled PDF, alongside the Chinese manual.
- Package tests pass under pdfLaTeX, XeLaTeX and LuaLaTeX, including CSV input.
- A pdfTeX CSV BOM compatibility issue was corrected. Only the Chinese manual
  uses the XeLaTeX/ctex workflow; the English manual builds with pdfLaTeX.
- Text files use LF-only line endings; .gitattributes keeps Git checkouts consistent.
- Both manual PDFs are built from the current 0.0.3 package.

## Package contents

Use a single top-level `gradbars/` directory. Include the .sty, LICENSE,
README.md, README.zh-CN.md, CHANGELOG.md, both current PDF manuals and their TeX
sources, the documentation data, layout sources/PDFs and build script required
to reproduce the manuals. Include linked documentation images.

Exclude .git, .github, .gitignore, .gitattributes, build products other than the
documentation PDFs, logs, auxiliary files, obsolete manual PDFs and this private
submission correspondence guide. Avoid duplicate files, non-ASCII filenames and
empty files/directories. Validate the files *inside* the ZIP for LF-only text.

## Upload form

If the package is still awaiting initial installation, explain that this upload
replaces the pending 0.0.1 submission. If CTAN has installed it in the meantime,
use the existing package's Upload link. Follow the CTAN team's instructions if
they ask for a particular workflow.

| Field | Value |
| --- | --- |
| Package id | gradbars |
| Version | 0.0.3 |
| Author / maintainer | SuFan |
| Your name | SuFan |
| Email | 3546236610@qq.com |
| Directory | /macros/latex/contrib/gradbars |
| License | MIT |
| Summary | Compact data graphics for LaTeX tables and inline text |
| Home / Repository | https://github.com/Tape5try/gradbars |
| Bugs | https://github.com/Tape5try/gradbars/issues |

Suggested English description:

> gradbars is a TikZ-based LaTeX package for compact graphics directly in table
> cells and inline text. It provides bars, signed stacks, layered and dumbbell
> comparisons, floating intervals, lollipops and sparklines. Shared scales,
> explicit missing values, formatted labels, targets, uncertainty markers,
> quality rules, CSV input and named category colors and textures are supported.
> The package is tested with pdfLaTeX, XeLaTeX and LuaLaTeX. Illustrated English
> and Chinese manuals include executable examples.

Suggested announcement:

> This submission replaces the pending initial gradbars 0.0.1 submission with
> version 0.0.3. New features include dumbbell comparisons, signed stacks,
> sparklines, target and interval quality rules, and semantic palettes with
> stable named category colors and patterns. English and Chinese PDF manuals
> are included. The package works with pdfLaTeX, XeLaTeX and LuaLaTeX; only the
> Chinese manual uses the XeLaTeX/ctex workflow.

Administrative note:

> This is a revised submission following Petra Ruebe-Pugliese's authorship and
> documentation questions about the pending 0.0.1 upload. Tape5try is SuFan's
> GitHub account. Please see our plain-text email reply for the confirmed
> authorship and maintenance details. Version 0.0.3 includes bilingual manuals
> and LF-only text files. Please replace the pending archive with this version.

## Plain-text reply draft

Change "will upload" to "have uploaded" only after the web upload succeeds.
If you can commit to long-term maintenance, also state that explicitly in your reply.

```text
Dear Petra,

Thank you for reviewing gradbars and for pointing out these issues.

Tape5try is my GitHub username, and my name is SuFan (苏凡).
I am the person who submitted the package using 3546236610@qq.com.

I am the author and maintainer of gradbars. The earlier phrase
"gradbars contributors" was an imprecise project-level attribution;
it has now been replaced with my name, SuFan. The LICENSE, READMEs,
package header and manuals now use consistent authorship information.

The package itself does not require XeLaTeX. I have tested it with
pdfLaTeX, XeLaTeX and LuaLaTeX, including CSV input, and corrected the
engine requirements in the documentation. The Chinese manual uses
XeLaTeX/ctex. An English manual and its PDF are now included and can be
built with pdfLaTeX.

All text files in the revised distribution use LF-only line endings.
The revised version is 0.0.3. I will upload the corrected archive through
the CTAN web form to replace the pending 0.0.1 submission.

Thank you for your time and help.

Kind regards,
SuFan
```

Official instructions: https://ctan.org/help/upload-pkg and
https://ctan.org/file/help/ctan/CTAN-upload-addendum .
