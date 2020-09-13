// init Masonry
var $grid = $('#grid').masonry({
    // options...
    columnWidth: '.grid-sizer',        
    itemSelector: '.grid-item',
    percentPosition: true,
    
});
// layout Masonry after each image loads
$grid.imagesLoaded().progress( function() {
    $grid.masonry('layout');
});


$('.add-to-watchlist').click(function(el) {
    const movieId = this.getAttribute('movieId');
    const tk = this.previousSibling.previousElementSibling.defaultValue;
    $.ajax({
        type: 'POST',
        url: `/watchlist/add/${movieId}/`,
        data: {'movie_id': movieId, 'csrfmiddlewaretoken': tk},
        dataType: 'json',
        success: function(resp) {
            if (resp.removed) {
                alert('Movie removed from watchlist.')
            } else {
                alert('Movie added to watchlist.')
            }
        },
        error: function(err) {
            alert("Login to add movies to watchlist.")
        }
    })

})

// hearts.forEach((el, ind) => {
//     $(el).click(function(){
//         const url_ = this.getAttribute("data-url");
//         const tk = $(this).attr("data-token");
//         const loading = document.createElement('span');

//         $.ajax({
//                  type: "POST",
//                  url: url_,
//                  data: {'slug': $(this).attr('name'), 'csrfmiddlewaretoken': tk},
//                  dataType: "json",
//                  beforeSend: function() {
//                     loading.innerHTML = `
//                     <div class="spinner-grow text-danger spinner-grow-sm" role="status">
//                     <span class="sr-only">Loading...</span>
//                     </div>
//                     `
//                     el.parentNode.replaceChild(loading, el)
//                  },
//                  complete: function(response) {
//                     setTimeout(() => {
//                         loading.parentNode.replaceChild(el, loading)
//                         likeRecipe(ind)
//                         document.getElementById(`likes-count-${response.responseJSON.liked_recipe}`).textContent = response.responseJSON.likes_count;
//                     }, 750);
//                 },
//                  success: function(response) {
//                      if (!response.logged_in) {
//                         window.location.replace(`http://localhost:8000/account/login/`);
//                      } else {
//                         let userLikes = document.getElementById(`user-likes-count`)
//                         if (userLikes) {
//                             userLikes.textContent = response.user_likes_count;
//                         }

//                      }
//                   },
//                   error: function() {
//                          alert('Someting went wrong. Try again later...')
//                   }
//             });

//       })
// });