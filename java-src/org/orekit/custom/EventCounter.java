package org.orekit.custom;

import org.orekit.propagation.SpacecraftState;
import org.orekit.time.AbsoluteDate;
import org.hipparchus.ode.events.Action;
import org.orekit.propagation.events.EventDetector;
import org.orekit.propagation.events.handlers.EventHandler;


public class EventCounter implements EventHandler{
    
        private int events = 0;
    
        public void init(SpacecraftState s0, AbsoluteDate t) {
            events = 0;
        }
    
        public Action eventOccurred(SpacecraftState s, EventDetector detector, boolean increasing) {
            if (increasing) {
                events++;
                return Action.CONTINUE;
            }
            return Action.CONTINUE;
        }
    
        public int getCount() {
            return events;
        }
    
}
