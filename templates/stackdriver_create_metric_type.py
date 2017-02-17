from google.cloud import monitoring
import sys

client = monitoring.Client()

def create_metric(metric, metric_kind, value_type, description) :
    descriptor = client.metric_descriptor(
        metric,
        metric_kind=metric_kind,
        value_type=value_type,
        description=description)
    descriptor.create()
    
def read_metric(metric) :
    query_results = client.query(metric, minutes=5)
    for result in query_results:
        print(result)

def main() :
    #create_metric('custom.googleapis.com/my_metric2',monitoring.MetricKind.GAUGE,monitoring.ValueType.DOUBLE, "test description.")
    read_metric(sys.argv[0])

if __name__ == "__main__":
    main()

