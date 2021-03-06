package au.com.codeka.warworlds.common.debug;

import com.squareup.wire.WireField;

import java.lang.reflect.Field;

import au.com.codeka.warworlds.common.proto.Packet;

/**
 * Helper class that contains some nice debugging details about our packets.
 */
public class PacketDebug {
  public static String getPacketDebug(Packet pkt, byte[] serialized) {
    StringBuilder sb = new StringBuilder();

    for (Field field : pkt.getClass().getFields()) {
      if (field.isAnnotationPresent(WireField.class)) {
        try {
          if (field.get(pkt) != null) {
            sb.append(field.getType().getSimpleName());
            sb.append(" ");
          }
        } catch (IllegalAccessException e) {
          // Ignore. (though should never happen)
        }
      }
    }

    sb.append("(");
    sb.append(serialized.length);
    sb.append(" bytes)");

    if (pkt.watch_sectors != null) {
      sb.append(" : [");
      sb.append(pkt.watch_sectors.left);
      sb.append(",");
      sb.append(pkt.watch_sectors.top);
      sb.append("] [");
      sb.append(pkt.watch_sectors.right);
      sb.append(",");
      sb.append(pkt.watch_sectors.bottom);
      sb.append("]");
    }
    if (pkt.star_updated != null) {
      sb.append(" : ");
      sb.append(pkt.star_updated.stars.size());
      sb.append(" stars");
    }

    return sb.toString();
  }
}
