var map;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: new google.maps.LatLng(-19.257753, 146.823688),
    zoom: 2,
    mapTypeId: 'terrain'
  });
  console.log('hello');
//  var kmlLayer = new google.maps.KmlLayer(src, {
//    suppressInfoWindows: true,
//    preserveViewport: false,
//    map: map
//  });
  kmlLayer.addListener('click', function(event) {
    var content = event.featureData.infoWindowHtml;
    var testimonial = document.getElementById('capture');
    testimonial.innerHTML = content;
  });
}