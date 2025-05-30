# Einführung

Durch Krankheit o.Ä. kann es sein, dass an einem Tag nicht genügend Personal zur Verfügung steht, um alle Kinder der 
Leolinos zu betreuen. In diesem Fall bestimmt die Kitaleitung, wieviele Gruppen betreut werden können und schreibt 
eine E-Mail an alle Eltern. In dieser Mail sind dann ein paar Gruppen von Kindern gelistet, die an dem Tag betreut 
werden können. Tatsächlich ist es aber so, dass eine maximale Anzahl an Kindern betreut werden kann, welche in der 
Regel nicht durch die Kinder in den genannten Gruppen erreicht wird. Dies kann drei Gründe haben
1. weil manche Kinder in mehreren Gruppen gelistet sind (Siehe dazu auch den Hinweis weiter unten)
2. weil die Gruppen nicht voll sind
3. weil gelistete Kinder an diesem Tag zu Hause bleiben (z.B. wegen Krankheit oder Urlaub).

D.h., es gibt typischerweise noch freie Plätze, die belegt werden können. Um die Vergabe dieser Plätze mit so wenig 
Aufwand wie möglich realisieren zu können, hat sich der Elternbeirat ein System ausgedacht und programmiert 
(siehe https://github.com/TaZi-loh/leolino-kids-prio ). Dieses System ist so gestaltet, dass alle Kinder, die nicht 
gelistet sind in eine Prioritätenliste einsortiert werden. Dabei stehen Kinder weiter oben, je öfter sie früher 
einen Platz aus einer gelisteten Gruppe angeboten haben. Kinder stehen weiter unten, je öfter sie früher einen 
freien Platz genutzt haben. Bei Gleichstand entscheidet ein Zufallsmechanismus.
Die freien Plätze werden nun einfach an die obersten Kinder der Prioritätenliste vergeben. Dazu erstellt 
Sebastian Ziesche typischerweise eine Ankündigung in der Gruppe "Ankündigungen".

# leolino-kids-prio

[![Release](https://img.shields.io/github/v/release/TaZi-loh/leolino-kids-prio)](https://img.shields.io/github/v/release/TaZi-loh/leolino-kids-prio)
[![Build status](https://img.shields.io/github/actions/workflow/status/TaZi-loh/leolino-kids-prio/main.yml?branch=main)](https://github.com/TaZi-loh/leolino-kids-prio/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/TaZi-loh/leolino-kids-prio/branch/main/graph/badge.svg)](https://codecov.io/gh/TaZi-loh/leolino-kids-prio)
[![Commit activity](https://img.shields.io/github/commit-activity/m/TaZi-loh/leolino-kids-prio)](https://img.shields.io/github/commit-activity/m/TaZi-loh/leolino-kids-prio)
[![License](https://img.shields.io/github/license/TaZi-loh/leolino-kids-prio)](https://img.shields.io/github/license/TaZi-loh/leolino-kids-prio)

Dieses Projekt dient zum Verwalten der Priorisierung der Leolino Kinder im Falle von Personalmangel

- **Github repository**: <https://github.com/TaZi-loh/leolino-kids-prio/>
- **Documentation** <https://TaZi-loh.github.io/leolino-kids-prio/>

## Getting started with your project

### 1. Create a New Repository

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:TaZi-loh/leolino-kids-prio.git
git push -u origin main
```

### 2. Set Up Your Development Environment

Then, install the environment and the pre-commit hooks with

```bash
make install
```

This will also generate your `uv.lock` file

### 3. Run the pre-commit hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```bash
uv run pre-commit run -a
```

### 4. Commit the changes

Lastly, commit the changes made by the two steps above to your repository.

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPI, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/codecov/).

## Releasing a new version



---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
