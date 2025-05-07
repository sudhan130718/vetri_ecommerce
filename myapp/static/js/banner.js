document.addEventListener("DOMContentLoaded", () => {
    let currentSlide = 0;
    const slider = document.querySelector('.slider');
    const totalSlides = document.querySelectorAll('.banner-img').length;

    setInterval(() => {
      currentSlide = (currentSlide + 1) % totalSlides;
      slider.style.transform = `translateX(-${currentSlide * 100}%)`;
    }, 3000); // Change every 3s
  });


  