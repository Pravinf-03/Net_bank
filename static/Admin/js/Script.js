
$(document).ready(function(){
    
    $(function(){
        var tDay = new Date();
        var day = tDay.getDate();
        var month =parseInt(tDay.getUTCMonth());
        var mon = month + 1;
        var year = tDay.getFullYear();
        var tDayStr = day+"-"+mon+"-"+year;
        $("#dateActOpen").val(tDayStr);
    });

    $("#dateBirth").change(function () { 
         
        var dob = $('#dateBirth').val();

        var age = calAge(dob);
            
        if(age <= 18){
            $("#coOwner").removeClass("d-none");
        }
        else{
            $("#coOwner").addClass("d-none");
        }
        
    });
    
});

/* function for calculating the age */

function calAge(dob){
    var date = new Date();
    var birthDate = new Date(dob);
    var year = date.getFullYear() - birthDate.getFullYear();
    return year
}