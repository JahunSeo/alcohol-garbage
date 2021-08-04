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
