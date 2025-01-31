$(document).ready(function () {

  $('#phoneMsg').text('');

  $('validMsg').text('');

  $('#secondaryMsg').text('');

  $("#id_phone_number").keypress(function(event) {
    return /\d/.test(String.fromCharCode(event.keyCode));
  });

$("#id_secondary_number").keypress(function(event) {
    return /\d/.test(String.fromCharCode(event.keyCode));
 });

  $("#id_location").keypress(function(event) {
    return /\D/.test(String.fromCharCode(event.keyCode));
  });

  $("#id_name").keypress(function(event) {
    return /\D/.test(String.fromCharCode(event.keyCode));
  });


  var phoneFinalVar;
  var secondaryFinalVar;
  var input = document.querySelector("#id_phone_number");
  var secondaryInput = document.querySelector("#id_secondary_number");

  var iti = window.intlTelInput(input, {
    autoPlaceholder: "polite",
    separateDialCode: true,
    initialCountry: 'UG',
    placeholderNumberType: 'MOBILE',
    preferredCountries: ["ug", 'ke', 'tz', 'rw'],
    utilsScript: "utils.js",

  });

  var secondary = window.intlTelInput(secondaryInput, {
    autoPlaceholder: "polite",
    separateDialCode: true,
    initialCountry: 'UG',
    placeholderNumberType: 'MOBILE',
    preferredCountries: ["ug", 'ke', 'tz', 'rw'],
    utilsScript: "utils.js",

  });

  var errorMap = ["Invalid number", "Invalid country code", "Too short", "Too long"];

  $("#id_phone_number").on('input', function(){
    if (input.value.trim()) {
      if (iti.isValidNumber()) {
        $('#phoneMsg').text('');
        $('#phoneMsg').text('Valid');
        $("#phoneMsg").css("color", "green");

        $('#validMsg').text('');
        $('#validMsg').text('Valid');
        $('#validMsg').css("color", "green");

        phoneFinalVar = iti.getNumber();
        document.getElementById("btn-submit").disabled = false;
        document.getElementById("btn-contact").disabled = false;

      }
      else {
        var errorCode = iti.getValidationError();
        $('#phoneMsg').text('');
        $('#phoneMsg').text(errorMap[errorCode]);
        $("#phoneMsg").css("color", "red");

        $('#validMsg').text('');
        $('#validMsg').text(errorMap[errorCode]);
        $('#validMsg').css("color", "red");

        document.getElementById("btn-submit").disabled = true;
        document.getElementById("btn-contact").disabled = true;
      }
    }

  });

   $("#id_secondary_number").on('input', function(){
        if (secondaryInput.value.trim()) {
          if (secondary.isValidNumber()) {
            $('#secondaryMsg').text('');
            $('#secondaryMsg').text('Valid');
            $("#secondaryMsg").css("color", "green");

            secondaryFinalVar = secondary.getNumber();

            document.getElementById("btn-submit").disabled = false;
            document.getElementById("btn-contact").disabled = false;

          }
          else {
            var errorCode = secondary.getValidationError();
            $('#secondaryMsg').text('');
            $('#secondaryMsg').text(errorMap[errorCode]);
            $("#secondaryMsg").css("color", "red");
            document.getElementById("btn-submit").disabled = true;
            document.getElementById("btn-contact").disabled = true;
          }
        }

      });


  $('#btn-contact').on('click', function(){
    if(input && secondaryInput){
        $("#id_phone_number").val(phoneFinalVar);
        $("#id_secondary_number").val(secondaryFinalVar)
    }
  });

  
  
});

