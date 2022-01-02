# Polish Law

[![CI](https://github.com/lawpeople/polish-law/actions/workflows/ci.yml/badge.svg)](https://github.com/lawpeople/polish-law/actions/workflows/ci.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/lawpeople/polish-law/main.svg)](https://results.pre-commit.ci/latest/github/lawpeople/polish-law/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/lawpeople/polish-law/)

Based on data provided by [Journal of Laws](https://dziennikustaw.gov.pl) and [ISAP](https://isap.sejm.gov.pl).

This project ultimately aims to provide a complete history of the law in Poland, however right now it focus on the legal acts published in the **Journal of Laws of the Republic of Poland**. Therefore the current scope of the history of the law is going to start in 1918. Every commit in the data repository provides a single legal act and changes in existing legal acts if any have been made. All of the commits are cryptographically signed by GPG key of the maintainer to confirm identity and improve confidence in data provided by the repositories. Commits provide additional metadata related to the introduced legal act and so every commit's description contains the following structure:

```
Dz.U. [Journal Year] nr [Journal Volume] poz. [Journal Position]

[Title of the legal act]
URL: [Official URL of the legal act published in the Journal of Laws]
Data ogłoszenia: [Promulgation date]
Data wydania: [Announcement date]
Data wejścia w życie: [Date when the act comes into force]
Data obowiązywania: [Effective date]
Organ wydający: [Issuing authority]
Organ zobowiązany: [Obliged authority]
Organ uprawniony: [Authorized body]
Podstawa prawna: [Legal basis]
Akty zmienione: [Amended acts]
Akty uchylone: [Repealed acts]
Akty uznane za uchylone: [Acts recognized as repealed]
```

Not all of these data fields have to appear in every commit. Some of them, such as the address in the **Journal of Laws** or title of the act, are always present. On the other hand legal acts do not always amend or repeal other acts, so therefore these fields are optional.

## Goals

The repository is currently in a state of heavy work in progress. Some of the necessary tools are integrated, there are a few tests and even some legal documents are already committed, however this is still in very early stages and does not represent the final vision.

At this point of development it is necessary to OCR the data out of the PDF documents and correct any mistakes by scripts and manual work, because old legal acts are only available as scanned PDFs. When all of those historical documents are converted to open text format the work on full automation will start to commit legal acts through Pull requests by a bot that will watch for events related to the legal acts through data sources made available by the Polish Parliament. Pull requests will contain data on newly introduced, amended and repealed acts, but will also include data such as vote results, status' or MP statements during readings.

In the future I will work on the final goal i.e. R&D project exposing the data through some kind of interface e.g. a website or a mobile app to simplify and enable access to the law for the public. The mission of this project is to empower people to learn knowledge that so far have been considered as too difficult and only for particular groups of people. The law is a public good and should be available to everyone and accessible by everyone, just like any other public services. All of the data provided in the repositories will always be available to everyone without any limit for free.

## Development

Pull requests that provide more tests or that enhance the tooling are very welcome.

Community Pull requests to the https://github.com/lawpeople/polish-law-data repository are prohibited.

## Why Markdown

Markdown is light on syntax, easy to parse and allows to quickly extract the text out of a document, while supporting necessary format features such as headings or even tables. It is widely recognized and used for documentation purposes and sometimes even simple books. Brief research concluded that Markdown has enough features in its syntax to support the needs of this project. Even if during the development it would turn out that it's not enough, converting to other format should be very easy.

## Existing projects

There are some products that already provide access to the text versions of legal acts from the **Journal of Laws** along with some metadata, but this project is most likely the first to tackle open source representation of the law in Poland as a git repository.