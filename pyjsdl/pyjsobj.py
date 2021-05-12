#Pyjsdl - Copyright (C) 2013 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

import pyjsdl.pyjs.DOM
import pyjsdl.pyjs.Window
import pyjsdl.pyjs.ui.RootPanel
import pyjsdl.pyjs.ui.FocusPanel
import pyjsdl.pyjs.ui.VerticalPanel
import pyjsdl.pyjs.Canvas.Color
import pyjsdl.pyjs.Canvas.ImageLoader
import pyjsdl.pyjs.ui.TextBox
import pyjsdl.pyjs.ui.TextArea
import pyjsdl.pyjs.ui.Event
import pyjsdl.pyjs.ui.MouseListener
import pyjsdl.pyjs.Canvas.HTML5Canvas
import pyjsdl.pyjs.media.Audio

DOM = pyjsdl.pyjs.DOM
Window = pyjsdl.pyjs.Window
RootPanel = pyjsdl.pyjs.ui.RootPanel.RootPanel
FocusPanel = pyjsdl.pyjs.ui.FocusPanel.FocusPanel
VerticalPanel = pyjsdl.pyjs.ui.VerticalPanel.VerticalPanel
Color = pyjsdl.pyjs.Canvas.Color.Color
loadImages = pyjsdl.pyjs.Canvas.ImageLoader.loadImages
TextBox = pyjsdl.pyjs.ui.TextBox.TextBox
TextArea = pyjsdl.pyjs.ui.TextArea.TextArea
Event = pyjsdl.pyjs.ui.Event
MouseWheelHandler = pyjsdl.pyjs.ui.MouseListener.MouseWheelHandler
HTML5Canvas = pyjsdl.pyjs.Canvas.HTML5Canvas.HTML5Canvas
Audio = pyjsdl.pyjs.media.Audio.Audio


def doc():
    return document


def get_main_frame():
    return document


def wnd():
    return window


def eventGetMouseWheelVelocityY(evt):
    #code from pyjs
    __pragma__('js', {},
        "return Math['round'](-evt['wheelDelta'] / 40) || 0;")


def requestAnimationFrameInit():
    requestAnimationFramePolyfill()
    return wnd()


def performanceNowInit():
    performanceNowPolyfill()
    return wnd()


def requestAnimationFramePolyfill():
    __pragma__('js', {},
    """
// http://paulirish.com/2011/requestanimationframe-for-smart-animating/
// http://my.opera.com/emoller/blog/2011/12/20/requestanimationframe-for-smart-er-animating

// requestAnimationFrame polyfill by Erik Möller. fixes from Paul Irish and Tino Zijdel

// MIT license

(function() {
    var lastTime = 0;
    var vendors = ['ms', 'moz', 'webkit', 'o'];
    for(var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
        window.requestAnimationFrame = window[vendors[x]+'RequestAnimationFrame'];
        window.cancelAnimationFrame = window[vendors[x]+'CancelAnimationFrame'] 
                                   || window[vendors[x]+'CancelRequestAnimationFrame'];
    }
 
    if (!window.requestAnimationFrame)
        window.requestAnimationFrame = function(callback, element) {
            var currTime = new Date().getTime();
            var timeToCall = Math.max(0, 16 - (currTime - lastTime));
            var id = window.setTimeout(function() { callback(currTime + timeToCall); }, 
              timeToCall);
            lastTime = currTime + timeToCall;
            return id;
        };
 
    if (!window.cancelAnimationFrame)
        window.cancelAnimationFrame = function(id) {
            clearTimeout(id);
        };
}());
    """)


def performanceNowPolyfill():
    __pragma__('js', {},
    """
// @license http://opensource.org/licenses/MIT
// copyright Paul Irish 2015


// Date.now() is supported everywhere except IE8. For IE8 we use the Date.now polyfill
//   github.com/Financial-Times/polyfill-service/blob/master/polyfills/Date.now/polyfill.js
// as Safari 6 doesn't have support for NavigationTiming, we use a Date.now() timestamp for relative values

// if you want values similar to what you'd get with real perf.now, place this towards the head of the page
// but in reality, you're just getting the delta between now() calls, so it's not terribly important where it's placed


(function(){

  if ("performance" in window == false) {
      window.performance = {};
  }
  
  Date.now = (Date.now || function () {  // thanks IE8
	  return new Date().getTime();
  });

  if ("now" in window.performance == false){
    
    var nowOffset = Date.now();
    
    if (performance.timing && performance.timing.navigationStart){
      nowOffset = performance.timing.navigationStart
    }

    window.performance.now = function now(){
      return Date.now() - nowOffset;
    }
  }

})();
    """)


fabs = Math.abs

