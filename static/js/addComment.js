// class AddComments {
//   constructor() {
//     this.$form = document.querySelector(".addComment");
//     this.setEvents();
//   }

//   setEvents() {
//     this.$form.addEventListener("submit", this.handleClickAdd);
//   }

//   handleClickAdd = (e) => {
//     e.preventDefault();
//     const formData = new FormData(this.$form);
//     const data = Array.from(formData.entries()).reduce(
//       (acc, [key, value]) => ({ ...acc, [key]: value }),
//       {},
//     );
//   };
// }

function submitComment() {
  console.log("submit comment!");
  let comment = $("#review-comment").val();
  console.log(comment);
  let data = {};
}

function submitSignUp() {
  $.ajax({
    type: "POST",
    url: "/api/user/register",
    data: {
      username: $("#signUp-username-box").val(),
      password: $("#signUp-password-box").val(),
    },
    success: function (response) {
      console.log(response);
      if (response["status"] == 200) {
        alert("회원가입이 완료되었습니다.");
        window.location.href = "/";
      } else {
        alert(response["msg"]);
      }
    },
  });
}
