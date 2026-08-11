// Pandoc custom template for a Japanese JIS B5 technical book.

#let book(
  title: [],
  subtitle: [],
  author: [],
  date: [],
  version: [],
  publisher: [],
  cover-image: none,
  body,
) = {
  set page(
    paper: "jis-b5",
    margin: (top: 25mm, bottom: 25mm, inside: 22mm, outside: 18mm),
    numbering: "1",
    number-align: center,
    header: context {
      let page-number = counter(page).get().first()
      if page-number > 1 {
        set text(size: 8pt, fill: luma(120))
        if calc.odd(page-number) {
          h(1fr) + emph(title)
        } else {
          emph(title) + h(1fr)
        }
        v(-4pt)
        line(length: 100%, stroke: 0.5pt + luma(200))
      }
    },
  )

  set text(font: ("Noto Sans CJK JP", "Noto Sans JP"), size: 10pt, lang: "ja")
  set heading(numbering: "1.1.")
  set par(leading: 0.85em, first-line-indent: (amount: 1em, all: true), justify: true)
  set list(indent: 1em, body-indent: 0.5em)
  set enum(indent: 1em, body-indent: 0.5em)

  show heading.where(level: 1): item => {
    pagebreak(weak: true)
    v(40pt)
    set text(size: 20pt, weight: "bold")
    block(width: 100%, below: 20pt, {
      if item.numbering != none {
        text(fill: rgb("#2b5797"), [第#counter(heading).display("1")章])
        v(8pt)
      }
      text(item.body)
      v(8pt)
      line(length: 100%, stroke: 2pt + rgb("#2b5797"))
    })
  }
  show heading.where(level: 2): item => {
    v(16pt)
    set text(size: 14pt, weight: "bold")
    block(below: 10pt, text(fill: rgb("#2b5797"), item.body))
  }
  show heading.where(level: 3): item => {
    v(10pt)
    set text(size: 12pt, weight: "bold")
    block(below: 8pt, item.body)
  }
  show raw.where(block: true): item => {
    set text(font: ("JetBrains Mono", "Noto Sans Mono CJK JP"), size: 8.5pt)
    block(
      width: 100%,
      fill: luma(245),
      inset: 10pt,
      radius: 4pt,
      stroke: 0.5pt + luma(220),
      item,
    )
  }
  show raw.where(block: false): item => {
    set text(font: ("JetBrains Mono", "Noto Sans Mono CJK JP"), size: 9pt)
    box(fill: luma(240), inset: (x: 3pt, y: 1pt), radius: 2pt, item)
  }
  show link: item => {
    set text(fill: rgb("#2b5797"))
    underline(item)
  }

  page(numbering: none, margin: 0pt, {
    if cover-image != none {
      align(center + horizon, image(cover-image, height: 100%, fit: "contain"))
    } else {
      rect(width: 100%, height: 100%, fill: rgb("#2b5797"), {
        align(center + horizon, {
          text(size: 14pt, fill: white, subtitle)
          v(10pt)
          text(size: 28pt, fill: white, weight: "bold", title)
          v(30pt)
          line(length: 40%, stroke: 1pt + white)
          v(20pt)
          text(size: 14pt, fill: white, author)
          v(8pt)
          text(size: 10pt, fill: white.transparentize(30%), date)
          if version != [] {
            v(4pt)
            text(size: 9pt, fill: white.transparentize(40%), version)
          }
        })
      })
    }
  })

  page({
    heading(outlined: false, numbering: none, [目次])
    outline(indent: auto, depth: 3)
  })

  body

  pagebreak()
  v(1fr)
  line(length: 100%, stroke: 0.5pt + luma(180))
  v(8pt)
  text(size: 16pt, weight: "bold", title)
  v(12pt)
  set text(size: 9pt)
  table(
    columns: (auto, 1fr),
    stroke: none,
    row-gutter: 4pt,
    [発行日], date,
    [著者], author,
    [発行], publisher,
    [版], version,
  )
  v(8pt)
  line(length: 100%, stroke: 0.5pt + luma(180))
}

#show: document => book(
  title: [$title$],
  subtitle: [$if(subtitle)$$subtitle$$endif$],
  author: [$for(author)$$author$$sep$, $endfor$],
  date: [$if(date)$$date$$endif$],
  version: [$if(version)$$version$$endif$],
  publisher: [$if(publisher)$$publisher$$endif$],
  cover-image: $if(cover-image)$"$cover-image$"$else$none$endif$,
  document,
)

$body$
