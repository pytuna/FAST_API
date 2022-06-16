const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);

const time = $('.time');
const sub1 = $('#sub1');
const sub12 = $('#sub12');
const sttConnection = $('.statusConnection');
const login = $('#login-btn');
const home = $('.row');
const homePage = $('#home');
const loginForm = $('.main-login');
const logined = $("#user");


login.onclick = () => {
  login.parentElement.classList.add('active');
  
  loginForm.classList.remove('hidden');
  
  
}
// fetch("test.json")
//   .then(response => response.json())
//   .then(json => {
      
//     if((json.sub1)===1) {
//         sub1.style.color = '#007f00';
//         console.log("test api")
//     }
//     if((json.sub12)===1) {
//         sub12.style.color = '#007f00';
//         console.log("test api12")
//     }
//     if((json.stt)===1) {
//         sttConnection.textContent = "Trạng thái kết nối: Đã kết nối";
//         console.log("test api3");
//     }
//   });
  
