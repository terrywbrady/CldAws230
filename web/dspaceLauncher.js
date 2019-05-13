// API_BASE will be set in dspaceLauncher.init.js
var PRS;
$(document).ready(function(){
  $("#refresh").on("click", function(){refresh();});
  refresh();
  loadPRs();
  $("#startInstance")
    .on("click", function(){
      startInstance();
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
        .append($("<td/>").text(obj['name']))
        .append(tdstate)
        .append(tddns)
        .append($("<td/>").text(obj['endTime']));
    }
    $("#startInstance").attr("disabled", (data.length >= 2));
  });
}

function loadPRs() {
  $.getJSON(API_BASE+"/projgetprs", function(data){
    if (data == null) return;
    PRS=data;
    $("#pr option").remove();
    for(var i=0; i<data.length; i++) {
      var row=data[i];
      var str = row.prnum + "; " + row.base + "; " + row.title;
      var opt = $("<option/>")
        .attr("value", i)
        .text(str);
      $("#pr").append(opt);
    }
  });
}

function stopInstance(id) {
  $.getJSON(API_BASE+"/projstopinstances?id="+id, function(data){
    setTimeout(refresh(), 2000);
  });
}

function startInstance(){
  $("#startInstance").attr("disabled", true);
  var data = {}
  var i = $("#pr").val();
  if (i>=0 && i<PRS.length) {
    data = PRS[i];
  }
  $.ajax({
    type: "POST",
    url: API_BASE+"/projcreateinstance",
    data: data,
    success: function(){
      setTimeout(function(){refresh()}, 2000);
    },
    failure: function() {
      alert("Instance Start Failed");
      refresh();
    },
    dataType: "json"
  });
}