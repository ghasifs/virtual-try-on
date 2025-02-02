// Function to generate linear gradient backgrounds with multiple browser prefixes
function background(c1, c2) {
  return {
    background: '-moz-linear-gradient(15deg, ' + c1 + ' 50%, ' + c2 + ' 50.1%)',
    background: '-o-linear-gradient(15deg, ' + c1 + ', ' + c2 + ' 50.1%)',
    background: '-webkit-linear-gradient(15deg, ' + c1 + ' 50%, ' + c2 + ')',
    background: '-ms-linear-gradient(15deg, ' + c1 + ' 50%, ' + c2 + ' 50.1%)',
    background: 'linear-gradient(15deg, ' + c1 + ' 50%,' + c2 + ' 50.1%)'
  }
}

// Function to change the background of elements with a fade-in effect
function changeBg(c1, c2) {
  $('div.bg').css(background(c1, c2)).fadeIn(700, function() {
    $('body').css(background(c1, c2));
    $('.bg').hide();
  })


  // Update the span.bg element with a different gradient direction
  $('span.bg').css({
    background: '-moz-linear-gradient(135deg, ' + c1 + ', ' + c2 + ')',
    background: '-o-linear-gradient(135deg, ' + c1 + ', ' + c2 + ')',
    background: '-webkit-linear-gradient(135deg, ' + c1 + ', ' + c2 + ')',
    background: '-ms-linear-gradient(135deg, ' + c1 + ', ' + c2 + ')',
    background: 'linear-gradient(135deg, ' + c1 + ',' + c2 + ')'
  });
}

// Declare a global variable to hold the current shirt ID
let currentShirtId = '';

// Initialize the slider with specific options
$slider = $('.slider');

$slider.slick({
  arrows: false,
  dots: true,
  infinite: true,
  speed: 600,
  fade: true,
  focusOnSelect: true,
  customPaging: function(slider, i) {
    var color = $(slider.$slides[i]).data('color').split(',')[1];
    return '<a><svg width="100%" height="100%" viewBox="0 0 16 16"><circle cx="8" cy="8" r="6.215" stroke="' + color + '"></circle></svg><span style="background:' + color + '"></span></a>';
  }
}).on('beforeChange', function(event, slick, currentSlide, nextSlide) {
  // Update shirt ID and colors on slide change
  currentShirtId = $('figure', $slider).eq(nextSlide).attr('id');

  colors = $('figure', $slider).eq(nextSlide).data('color').split(',');
  color1 = colors[0];
  color2 = colors[1];

  // Update UI elements with new colors
  $('.price, .btn, .switch-label').css({
    color: color1
  });
  changeBg(color1, color2);
  $('.btn').css({
    borderColor: color2
  });
});

// Function to retrieve the currently selected radio button for switches
function getSelectedSwitch() {
  const selected = document.querySelector('input[name="switch"]:checked');
  return selected ? selected.id : null; // Return the ID of the selected radio button
}

// Add event listeners after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('video-modal');
  const videoOutput = document.getElementById('video-output');
  const tryOnButton = document.getElementById('try-on-btn');
  const closeButton = document.querySelector('.close');

  // Show modal on try-on button click
  tryOnButton.addEventListener('click', () => {
    const shirtId = currentShirtId || 'shirt_natural'; // Default to 'shirt_natural'
    const selectedModel = getSelectedSwitch() || 'Pose'; // Default to 'Pose'

    // Display modal and start video feed with shirt ID and model
    modal.style.display = 'block';
    videoOutput.src = `/video_feed?shirt_id=${shirtId}&model=${selectedModel}`;

    console.log(`Video feed started with shirt ID: ${shirtId} and model: ${selectedModel}`);
  });

  // Hide modal and stop video feed on close button click
  closeButton.addEventListener('click', () => {
    modal.style.display = 'none';
    videoOutput.src = ''; // Stop video feed
  });

  // Hide modal when clicking outside modal content
  window.addEventListener('click', (event) => {
    if (event.target === modal) {
      modal.style.display = 'none';
      videoOutput.src = ''; // Stop video feed
    }
  });
});