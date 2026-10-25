# Toolkit icon sources

The profile uses path-based SVG assets for its toolkit. No raster favicons are embedded in SVG wrappers. The displayed variants keep the underlying vector geometry and use proportional viewports with a stable contrasting backing for dark and light pages.

- Programming, design and development-tool marks: [Devicon](https://github.com/devicons/devicon), pinned at `6a37858047b0e8d9c9c0e68f4a071fc410652e89`. The exact [MIT notice](../assets/toolkit/DEVICON-LICENSE.txt) is retained.
- OpenFOAM and AVL: official website vector pinned-tab marks.
- CONVERGE: official vector wordmark, displaying its left-hand emblem.
- ParaView: official vector logo, displaying the three-stripe emblem.
- Siemens and GNU Octave: official vector assets.
- Ansys, AutoCAD, Autodesk, COMSOL and Dassault Systèmes: [Simple Icons](https://github.com/simple-icons/simple-icons), pinned at `90646e4bf7f3b89df6c37e65baf3e7bc759a517c`, under [CC0](https://github.com/simple-icons/simple-icons/blob/90646e4bf7f3b89df6c37e65baf3e7bc759a517c/LICENSE.md).
- Fusion: the product-specific SVG from the Devicon project.

Corporate marks identify their vendor: the Ansys mark accompanies Fluent, CFX and EnSight; Siemens accompanies NX and STAR-CCM+; Dassault Systèmes accompanies SolidWorks. These are not distinct product certification badges.

SU2, Tecplot 360 and OriginPro remain readable text links because no reliable vector product asset was found for this edition. Basilisk and Palabos use an original generic flow symbol rather than an invented vendor logo.

Exact source URLs, source hashes, published hashes and processing details for every displayed SVG are in [icon-sources.json](../assets/toolkit/icon-sources.json).

The toolkit adds a verification and reproducibility group for Git, Linux, GitHub Actions, pytest and CMake, reflecting the existing projects' development and checking workflows. CATIA is removed at the owner's request.
