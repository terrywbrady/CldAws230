// API_BASE will be set in dspaceLauncher.init.js
$(document).ready(function(){
  refresh();
  $("#startInstance")
    .on("click", function(){
      $.ajax({
        type: "POST",
        url: API_BASE+"/projcreateinstance",
        data: {},
        success: function(){
          setTimeout(2000, function(){refresh()});
        },
        failure: function() {
          alert("Instance Start Failed");
          refresh();
        },
        dataType: "json"
      });
    });
});

function refresh() {
  $.getJSON(API_BASE+"/projListInstances", function(data){
    if (data == null) return;
    $("#instances tr.data").remove();
    for(var i=0; i<data.length; i++) {
      var tr = $("<tr class='data'/>");
      $("#instances table").append(tr);
      var obj = data[i];
      var tddns = $("<td/>")
        .append($("<a/>")
          .text(obj['dns'])
          .attr("href", "http://"+obj['dns']+":8080/xmlui")
        );
      var tdstate = $("<td/>")
        .text(obj['state']+" ")
        .append(
          $("<button class='stop'/>")
            .text("Stop")
            .attr("id", obj['id'])
            .on("click", function(){
              $(this).attr("disabled", true);
              stopInstance($(this).attr("id"))
            })
        );

      tr.append($("<td/>").text(obj['id']))
        .append(tdstate)
        .append(tddns)
        .append($("<td/>").text(obj['launchTime']))
        .append($("<td/>").text(obj['endTime']));
    }
    $("#startInstance").attr("disabled", (data.length >= 2));
  });
}

function stopInstance(id) {
  $.getJSON(API_BASE+"/projstopinstances?id="+id, function(data){
    setTimeout(2000, refresh());
  });
}
