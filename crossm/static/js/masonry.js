window.onload = () => {
    masonry = new Masonry('.grid', {
    gutter: '.gutter-sizer',
    itemSelector: '.grid-item',
    columnWidth: '.grid-sizer',
    percentPosition: true,
    transitionDuration: '0.2s', 
  });
};