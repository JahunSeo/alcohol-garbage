function addReview() {
  console.log({
    username: $("#commentUser").attr("data-id"),
    beer_id: $("#beerName").attr("data-id"),
    score: $("input[name=rating]:checked").val(),
    comment: $("#review-comment").val(),
  });
  $.ajax({
    type: "POST",
    url: "/api/review/add",
    data: {
      username: $("#commentUser").attr("data-id"),
      beer_id: $("#beerName").attr("data-id"),
      score: $("input[name=rating]:checked").val(),
      comment: $("#review-comment").val(),
    },
    success: function (response) {
      console.log(response);
      if (response["status"] == 200) {
        alert("리뷰 업로드가 완료되었습니다.");
        window.location.reload();
      } else {
        alert(response["msg"]);
      }
    },
  });
}

// function deleteReview(id) {
//   $.ajax({
//     type: "POST",
//     url: "/api/review/delete",
//     data: {
//       username: id,
//     },
//     success: function (response) {
//       console.log(response);
//       if (response["status"] == 200) {
//         alert("리뷰 삭제가 완료 되었습니다");
//         window.location.reload();
//       } else {
//         alert(response["msg"]);
//       }
//     },
//   });
// }
