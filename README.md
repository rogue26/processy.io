[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/rogue26/processy.io">
    <img src="static/img/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Processy.io</h3>

  <p align="center">
    Open-source project and knowledge management
    <br />
    <a href="https://github.com/rogue26/processy.io"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/rogue26/processy.io">View Demo</a>
    ·
    <a href="https://github.com/rogue26/processy.io/issues">Report Bug</a>
    ·
    <a href="https://github.com/rogue26/processy.io/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Project management, project scoping, and knowledge management are so closely related that a project-oriented 
organization is unlikely to excel at **any** of them unless it excels at **all** of them.

There are many great project management tools out there that are well-suited for their intended purposes. I wanted a 
tool that more tightly integrated project management, knowledge management, and project scoping.

While Processy.io was built with the needs of a project-oriented, consulting-ish organization in mind, the structure 
that is imposed on tasks, deliverables, and workstreams, as well as the integrated project management tools make it 
useful for a much broader range of activities.



### Built With

* [Django](https://www.djangoproject.com/)
* [JQuery](https://jquery.com)
* [Bootstrap](https://getbootstrap.com)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Processy.io is a webapp written in [Python](https://python.org), which is accessed through the browser while running 
a local server. To run the webapp, you'll need to have python installed on your computer. Python is preinstalled on 
MacOS and virtually all Linux distributions. You can get the latest Python installation materials for Windows 
[here](https://www.python.org/downloads/windows/).


### Installation

1. Navigate to your preferred directory (any directory will do) and clone the repo
   ```sh
   git clone https://github.com/rogue26/processy.io.git
   ```
   Alternatively, you can download the code as a zip file from github.
2. Create a virtual environment
   ```sh
   python -m venv env
   ```
3. Activate the virtual environment. On Windows, type:
   ```sh
   env\Scripts\activate.bat
   ```
   On Linux or Mac, type:
   ```sh
   env/bin/activate
   ```
4. Install the required python packages
   ```sh
   pip install -r requirements.txt
   ```
5. Standard Django startup procedures, i.e.
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
6. Navigate to [localhost:8000](localhost:8000) in your browser.



<!-- USAGE EXAMPLES -->
## Usage

Coming soon.

<!-- Use this space to show useful examples of how a project can be used. Additional screenshots, code 
examples and demos work well in this space. You may also link to more resources. -->

<!-- _For more examples, please refer to the [Documentation](https://example.com)_ -->



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/rogue26/processy.io/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Django Bootstrap Modal Forms](https://github.com/trco/django-bootstrap-modal-forms) is a fantastic, well-constructed 
Django app that makes it effortless to use Bootstrap 4 modals with ajax within Django.

* [Frappe Gantt](https://github.com/frappe/gantt) is an excellent javascript Gantt chart plugin with everything you 
need and nothing you don't.




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/rogue26/processy.io.svg?style=for-the-badge
[contributors-url]: https://github.com/rogue26/processy.io/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/rogue26/processy.io.svg?style=for-the-badge
[forks-url]: https://github.com/rogue26/processy.io/network/members
[stars-shield]: https://img.shields.io/github/stars/rogue26/processy.io.svg?style=for-the-badge
[stars-url]: https://github.com/rogue26/processy.io/stargazers
[issues-shield]: https://img.shields.io/github/issues/rogue26/processy.io.svg?style=for-the-badge
[issues-url]: https://github.com/rogue26/processy.io/issues
[license-shield]: https://img.shields.io/github/license/rogue26/processy.io.svg?style=for-the-badge
[license-url]: https://github.com/rogue26/processy.io/blob/master/LICENSE.txt
