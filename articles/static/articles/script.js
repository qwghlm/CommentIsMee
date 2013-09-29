$(document).ready(function() {
  if (window.articleID !== undefined) {
    initTwitter();
  }
});

function clickEventToAnalytics (intentEvent) {
  if (!intentEvent) return;
  var label = intentEvent.region;
  ga('send', 'event', 'Twitter', intentEvent.type, label, articleID);
}
 
function tweetIntentToAnalytics (intentEvent) {
  if (!intentEvent) return;
  var label = "tweet";
  ga('send', 'event', 'Twitter', intentEvent.type, label, articleID);
}

var initCount = 0;
function initTwitter() {
  if (window.twttr === undefined || window.ga === undefined) {
    if (initCount++ < 60) {
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