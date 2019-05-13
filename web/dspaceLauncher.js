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
      var tddns = $("<td/>").text(obj['dns'].replace(/\..*$/,""))
      for(var j=0; j<data[i].services.length; j++){
        var sv = data[i].services[j];
        var url = "http://"+obj['dns']+sv.path;
        tddns.append($("<span> </span>"));
        tddns.append($("<a/>").text(sv.name).attr("href", url));
      }
      var tdact = $("<td/>")
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
        .append($("<td/>").text(obj['pr']))
        .append($("<td/>").text(obj['branch']))
        .append($("<td/>").text(obj['name']))
        .append($("<td/>").text(obj['state']))
        .append(tdact)
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
    data: JSON.stringify(data),
    dataType: "json",
    contentType: 'application/json',
    success: function(){
      setTimeout(function(){refresh()}, 2000);
    },
    failure: function() {
      alert("Instance Start Failed");
      refresh();
    }
  });
}
