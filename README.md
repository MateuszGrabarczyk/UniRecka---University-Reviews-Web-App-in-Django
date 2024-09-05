# UniRecka---University-Reviews-Web-App-in-Django

This project was done for my university thesis, therefore it's made in Polish.
The goal of this application is to help future students choose university.
Students can browse and search universities, browse the reviews that current students or people who graduated added.
This application was made in Django framework. Bootstrap helped to create unified interface. The application is responsive to different screen sizes.

Below you can find some screenshots from my application. Feel free to ask!

The main page:
![image](https://github.com/MateuszGrabarczyk/UniRecka---University-Reviews-Web-App-in-Django/assets/72306674/e2c42b7d-2faf-4fb7-ba69-388277a96bf0)

The search university page:
![image](https://github.com/MateuszGrabarczyk/UniRecka---University-Reviews-Web-App-in-Django/assets/72306674/9f4a6ca9-02e1-4231-9e95-b2ce1662b840)

The university page:
![image](https://github.com/MateuszGrabarczyk/UniRecka---University-Reviews-Web-App-in-Django/assets/72306674/9d686061-9d30-44af-90a1-19a9c3b84150)

## Installation and Setup using Docker

1. **Clone the repository:**

   ```bash
   git clone https://github.com/MateuszGrabarczyk/UniRecka---University-Reviews-Web-App-in-Django.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd unirecka
   ```

3. **Build the Docker Image:**

   ```bash
   docker-compose build
   ```

4. **Run the Docker Container:**

   ```bash
   docker-compose up
   ```

5. **Open your browser and visit:**

   ```bash
   http://localhost:8000
   ```

6. **Check whether superuser was created correctly:**

   ```bash
   http://localhost:8000/admin
   ```

   And log in using admin as username and admin as password.
