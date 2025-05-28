import pyshark
import pandas as pd

def extract_from_pcap(pcap_path, output_csv):
    cap = pyshark.FileCapture(pcap_path)
    records = []
    for pkt in cap:
        try:
            records.append({
                'src_ip': pkt.ip.src,
                'dst_ip': pkt.ip.dst,
                'src_port': int(pkt[pkt.transport_layer].srcport),
                'dst_port': int(pkt[pkt.transport_layer].dstport),
                'protocol': pkt.transport_layer,
                'packet_count': 1,
                'byte_count': int(pkt.length),
                'duration': float(pkt.sniff_timestamp)
            })
        except:
            continue
    df = pd.DataFrame(records)
    df = df.groupby(['src_ip','dst_ip','src_port','dst_port','protocol'], as_index=False).agg({
        'packet_count':'count',
        'byte_count':'sum',
        'duration': lambda x: x.max()-x.min()
    })
    df.to_csv(output_csv, index=False)
