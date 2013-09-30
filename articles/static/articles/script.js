var thisURL = window.location.pathname;

$(document).ready(function() {
  initTwitter();
});

function clickEventToAnalytics (intentEvent) {
  if (!intentEvent) { return; }
  var label = intentEvent.region;
  ga('send', 'event', 'Twitter', intentEvent.type, label, thisURL);
}
 
function tweetIntentToAnalytics (intentEvent) {
  if (!intentEvent) { return; }
  var label = "tweet";
  ga('send', 'event', 'Twitter', intentEvent.type, label, thisURL);
}

function facebookLikeToAnalytics (href, widget) {
  ga('send', 'event', 'Facebook', 'action', 'like', thisURL);
}

function facebookUnlikeToAnalytics (href, widget) {
  ga('send', 'event', 'Facebook', 'action', 'unlike', thisURL);
}

var initTwitterCount = 0;
function initTwitter() {
  if (window.twttr === undefined) {
    if (initTwitterCount++ < 60) {
      setTimeout(initTwitter, 500);
    }
  }
  else {
    twttr.ready(function (twttr) {
      twttr.events.bind('click', clickEventToAnalytics);
      twttr.events.bind('tweet', tweetIntentToAnalytics);
    });
  }
}

window.fbAsyncInit = function() {
  FB.Event.subscribe('edge.create', facebookLikeToAnalytics);
  FB.Event.subscribe('edge.remove', facebookUnlikeToAnalytics);
};