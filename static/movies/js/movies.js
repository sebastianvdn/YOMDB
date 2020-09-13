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

