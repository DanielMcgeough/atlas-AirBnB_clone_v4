window.addEventListener('load', function () {
    // task 2
    const amenityIds = {};
    $('input[type=checkbox]').change(function () {
      if ($(this).prop('checked')) {
        amenityIds[$(this).attr('data-id')] = $(this).attr('data-name');
      } else if (!$(this).prop('checked')) {
        delete amenityIds[$(this).attr('data-id')];
      }
      if (Object.keys(amenityIds).length === 0) {
        $('div.amenities h4').html('&nbsp');
      } else {
        $('div.amenities h4').text(Object.values(amenityIds).join(', '));
      }
    });
  });

  $(document).ready(function() {
    $.get('http://0.0.0.0:5001/api/v1/status/')
        .done(function (data, textStatus, xhr) {
          console.log(xhr.status);
            if(xhr.status == 200) {
             $('#api_status').addClass('available');
            } else {
             $('#api_status').removeClass('available');
            }
        })
  });