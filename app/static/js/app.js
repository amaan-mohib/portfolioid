const navSlide = () => {
  const burger = document.querySelector(".burger");
  const nav = document.querySelector(".nav-links");
  const navLinks = document.querySelectorAll(".nav-links li");

  burger.addEventListener("click", () => {
    //Toggle nav
    nav.classList.toggle("nav-active");

    //animate links
    navLinks.forEach((link, index) => {
      if (link.style.animation) {
        link.style.animation = "";
      } else {
        link.style.animation = `navLinkFade 0.5s ease forwards ${
          index / 7 + 0.3
        }s`;
      }
    });
    //burger anim
    burger.classList.toggle("toggle");
  });
};

const modal = () => {
  var modalBtn=document.querySelector('.modal-btn');
  var modalBg=document.querySelector('.modal-bg');
  var modalClose=document.querySelector('.modal-close');
  var modalCloseBtn=document.querySelector('.modal-close-btn');

  modalBtn.addEventListener('click',function(){
    modalBg.classList.add('modal-bg-active');
  });

  modalClose.addEventListener('click',function(){
    modalBg.classList.remove('modal-bg-active');
  });
  modalCloseBtn.addEventListener('click',function(){
    modalBg.classList.remove('modal-bg-active');
  });
};

navSlide();
modal();

