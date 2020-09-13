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

const _url = location.href
if (!_url.includes('page')) {
    location.href += '&page=1'
}