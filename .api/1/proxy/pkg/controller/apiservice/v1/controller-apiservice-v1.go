package controllerapiservicev1

import (
	"context"
	"fmt"
	"io/fs"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"time"

	grpcui "github.com/fullstorydev/grpcui/standalone"
	grpc_prometheus "github.com/grpc-ecosystem/go-grpc-prometheus"
	grpcgatewayruntime "github.com/grpc-ecosystem/grpc-gateway/v2/runtime"
	"github.com/prometheus/client_golang/prometheus/promhttp"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	authenticationbasic "dxnnymurphy.io/cryptodatastream/pkg/authentication/basic"
	"dxnnymurphy.io/cryptodatastream/pkg/configuration"
	model "dxnnymurphy.io/cryptodatastream/pkg/model/cryptodatastream/v3"
	"dxnnymurphy.io/cryptodatastream/pkg/resource"
)

type ControllerApiServiceV1 struct {
	AuthenticationBasic authenticationbasic.AuthenticationBasic
	Configuration       configuration.Configuration
}

func NewControllerApiServiceV1(ctx context.Context) (instance *ControllerApiServiceV1) {
	instance = &ControllerApiServiceV1{
		AuthenticationBasic: authenticationbasic.GetAuthenticationBasic(ctx, "v1"),
		Configuration:       configuration.GetConfiguration(ctx, "v1"),
	}

	return instance
}

func (_self *ControllerApiServiceV1) Start(ctx context.Context, err chan error) {
	go func() {
		for {
			time.Sleep(1 * time.Second)

			host := _self.Configuration.Get("controller.apiservice.host")
			port := _self.Configuration.Get("controller.apiservice.port")

			endpoint := fmt.Sprintf("%+v:%+v", host, port)

			mux := http.NewServeMux()

			func() {
				ops_monitoring_api_url := _self.Configuration.Get("controller.apiservice.ops.monitoring.api.url").(string)

				mux.Handle(ops_monitoring_api_url+"/", http.StripPrefix(ops_monitoring_api_url, promhttp.Handler()))

				log.Printf("Exposing Prometheus metrics for Ops Monitoring at http://%+v%+v \n", endpoint, ops_monitoring_api_url)
			}()

			func() {
				proxy_prometheus_url := _self.Configuration.Get("controller.apiservice.proxy.prometheus.url").(string)
				proxy_prometheus_target_host := _self.Configuration.Get("controller.apiservice.proxy.prometheus.target.host")
				proxy_prometheus_target_port := _self.Configuration.Get("controller.apiservice.proxy.prometheus.target.port")

				proxy_prometheus_target_endpoint := fmt.Sprintf("http://%+v:%+v", proxy_prometheus_target_host, proxy_prometheus_target_port)

				target_prometheus_url, _ := url.Parse(proxy_prometheus_target_endpoint)
				handler_for_proxy_prometheus := httputil.NewSingleHostReverseProxy(target_prometheus_url)

				mux.Handle(proxy_prometheus_url+"/", handler_for_proxy_prometheus)

				log.Printf("Starting proxy Prometheus service at http://%+v%+v \n", endpoint, proxy_prometheus_url)
			}()

			func() {
				proxy_grafana_url := _self.Configuration.Get("controller.apiservice.proxy.grafana.url").(string)
				proxy_grafana_target_host := _self.Configuration.Get("controller.apiservice.proxy.grafana.target.host")
				proxy_grafana_target_port := _self.Configuration.Get("controller.apiservice.proxy.grafana.target.port")

				proxy_grafana_target_endpoint := fmt.Sprintf("http://%+v:%+v", proxy_grafana_target_host, proxy_grafana_target_port)

				target_grafana_url, _ := url.Parse(proxy_grafana_target_endpoint)
				handler_for_proxy_grafana := httputil.NewSingleHostReverseProxy(target_grafana_url)

				mux.Handle(proxy_grafana_url+"/", handler_for_proxy_grafana)

				log.Printf("Starting proxy Grafana service at http://%+v%+v \n", endpoint, proxy_grafana_url)
			}()

			func() {
				proxy_kafka_url := _self.Configuration.Get("controller.apiservice.proxy.kafka.url").(string)
				proxy_kafka_target_host := _self.Configuration.Get("controller.apiservice.proxy.kafka.target.host")
				proxy_kafka_target_port := _self.Configuration.Get("controller.apiservice.proxy.kafka.target.port")

				proxy_kafka_target_endpoint := fmt.Sprintf("http://%+v:%+v", proxy_kafka_target_host, proxy_kafka_target_port)

				target_kafka_url, _ := url.Parse(proxy_kafka_target_endpoint)
				handler_for_proxy_kafka := httputil.NewSingleHostReverseProxy(target_kafka_url)

				mux.Handle(proxy_kafka_url+"/", http.StripPrefix(proxy_kafka_url, _self.AuthenticationBasic.EnableAuthenticationBasicForHttpHandler(ctx, "admin", handler_for_proxy_kafka)))

				log.Printf("Starting proxy Kafka service at http://%+v%+v \n", endpoint, proxy_kafka_url)
			}()

			func() {
				proxy_repo_url := _self.Configuration.Get("controller.apiservice.proxy.repo.url").(string)
				proxy_repo_target_host := _self.Configuration.Get("controller.apiservice.proxy.repo.target.host")
				proxy_repo_target_port := _self.Configuration.Get("controller.apiservice.proxy.repo.target.port")

				proxy_repo_target_endpoint := fmt.Sprintf("http://%+v:%+v", proxy_repo_target_host, proxy_repo_target_port)

				target_repo_url, _ := url.Parse(proxy_repo_target_endpoint)
				handler_for_proxy_repo := httputil.NewSingleHostReverseProxy(target_repo_url)

				mux.Handle(proxy_repo_url+"/", http.StripPrefix(proxy_repo_url, handler_for_proxy_repo))

				log.Printf("Starting proxy repo service at http://%+v%+v \n", endpoint, proxy_repo_url)
			}()

			func() {
				proxy_cli_url := _self.Configuration.Get("controller.apiservice.proxy.cli.url").(string)
				proxy_cli_target_host := _self.Configuration.Get("controller.apiservice.proxy.cli.target.host")
				proxy_cli_target_port := _self.Configuration.Get("controller.apiservice.proxy.cli.target.port")

				proxy_cli_target_endpoint := fmt.Sprintf("http://%+v:%+v", proxy_cli_target_host, proxy_cli_target_port)

				target_cli_url, _ := url.Parse(proxy_cli_target_endpoint)
				handler_for_proxy_cli := httputil.NewSingleHostReverseProxy(target_cli_url)

				mux.Handle(proxy_cli_url+"/", http.StripPrefix(proxy_cli_url, _self.AuthenticationBasic.EnableAuthenticationBasicForHttpHandler(ctx, "admin", handler_for_proxy_cli)))

				log.Printf("Starting proxy CLI service at http://%+v%+v \n", endpoint, proxy_cli_url)
			}()

			func() {
				proxy_kubernetesproxy_url := _self.Configuration.Get("controller.apiservice.proxy.kubernetesproxy.url").(string)
				proxy_kubernetesproxy_target_host := _self.Configuration.Get("controller.apiservice.proxy.kubernetesproxy.target.host")
				proxy_kubernetesproxy_target_port := _self.Configuration.Get("controller.apiservice.proxy.kubernetesproxy.target.port")

				proxy_kubernetesproxy_target_endpoint := fmt.Sprintf("http://%+v:%+v", proxy_kubernetesproxy_target_host, proxy_kubernetesproxy_target_port)

				target_kubernetesproxy_url, _ := url.Parse(proxy_kubernetesproxy_target_endpoint)
				handler_for_proxy_kubernetesproxy := httputil.NewSingleHostReverseProxy(target_kubernetesproxy_url)

				mux.Handle(proxy_kubernetesproxy_url+"/", http.StripPrefix(proxy_kubernetesproxy_url, _self.AuthenticationBasic.EnableAuthenticationBasicForHttpHandler(ctx, "admin", handler_for_proxy_kubernetesproxy)))

				log.Printf("Starting proxy KubernetesProxy service at http://%+v%+v \n", endpoint, proxy_kubernetesproxy_url)
			}()

			func() {
				proxy_sqlite_url := _self.Configuration.Get("controller.apiservice.proxy.sqlite.url").(string)
				proxy_sqlite_target_host := _self.Configuration.Get("controller.apiservice.proxy.sqlite.target.host")
				proxy_sqlite_target_port := _self.Configuration.Get("controller.apiservice.proxy.sqlite.target.port")

				proxy_sqlite_target_endpoint := fmt.Sprintf("http://%+v:%+v", proxy_sqlite_target_host, proxy_sqlite_target_port)

				target_sqlite_url, _ := url.Parse(proxy_sqlite_target_endpoint)
				handler_for_proxy_sqlite := httputil.NewSingleHostReverseProxy(target_sqlite_url)

				mux.Handle(proxy_sqlite_url+"/", _self.AuthenticationBasic.EnableAuthenticationBasicForHttpHandler(ctx, "admin", handler_for_proxy_sqlite))

				log.Printf("Starting proxy SQLite-UI (kcde-sandbox) at http://%+v%+v \n", endpoint, proxy_sqlite_url)
			}()

			func() {
				mux_api := grpcgatewayruntime.NewServeMux()

				proxy_grpc_target_host := _self.Configuration.Get("controller.apiservice.proxy.grpc.target.host")
				proxy_grpc_target_port := _self.Configuration.Get("controller.apiservice.proxy.grpc.target.port")

				proxy_grpc_target_endpoint := fmt.Sprintf("%+v:%+v", proxy_grpc_target_host, proxy_grpc_target_port)

				err_from_proxy_api2grpc := model.RegisterServiceCryptoDataStreamHandlerFromEndpoint(
					ctx,
					mux_api,
					proxy_grpc_target_endpoint,
					[]grpc.DialOption{
						grpc.WithTransportCredentials(insecure.NewCredentials()),
						grpc.WithUnaryInterceptor(grpc_prometheus.UnaryClientInterceptor),
					},
				)
				if err_from_proxy_api2grpc != nil {
					err <- err_from_proxy_api2grpc
				}

				mux.Handle("/", _self.AuthenticationBasic.EnableAuthenticationBasicForHttpHandler(ctx, "admin", mux_api))
			}()

			func() {
				fs_for_proxy_swagger, err_from_fs_for_proxy_swagger := fs.Sub(resource.PublicProxySwagger, "public/proxy/swagger")
				if err_from_fs_for_proxy_swagger != nil {
					err <- err_from_fs_for_proxy_swagger
				}
				handler_for_proxy_swagger := http.FileServer(http.FS(fs_for_proxy_swagger))

				proxy_swagger_url := _self.Configuration.Get("controller.apiservice.proxy.swagger.url").(string)

				mux.Handle(proxy_swagger_url+"/", http.StripPrefix(proxy_swagger_url, handler_for_proxy_swagger))

				log.Printf("Starting proxy Swagger-API service at http://%+v%+v \n", endpoint, proxy_swagger_url)
			}()

			func() {
				proxy_grpc_target_host := _self.Configuration.Get("controller.apiservice.proxy.grpc.target.host")
				proxy_grpc_target_port := _self.Configuration.Get("controller.apiservice.proxy.grpc.target.port")

				proxy_grpc_target_endpoint := fmt.Sprintf("%+v:%+v", proxy_grpc_target_host, proxy_grpc_target_port)

				var handler_for_proxy_grpc http.Handler
				for {
					grpcclient_for_proxy_grpc, err_from_grpcclient_for_proxy_grpc := grpc.Dial(
						proxy_grpc_target_endpoint,
						[]grpc.DialOption{
							grpc.WithTransportCredentials(insecure.NewCredentials()),
							grpc.WithUnaryInterceptor(grpc_prometheus.UnaryClientInterceptor),
						}...,
					)
					if err_from_grpcclient_for_proxy_grpc != nil {
						log.Printf("Failed to connect to gRPC server at %+v - %+v ... \n", proxy_grpc_target_endpoint, err_from_grpcclient_for_proxy_grpc)
					}

					var err_from_handler_for_proxy_grpc error
					handler_for_proxy_grpc, err_from_handler_for_proxy_grpc = grpcui.HandlerViaReflection(ctx, grpcclient_for_proxy_grpc, proxy_grpc_target_endpoint)
					if err_from_handler_for_proxy_grpc != nil {
						log.Printf("Failed to connect to gRPC server at %+v - %+v | Retrying in 5 seconds ... \n", proxy_grpc_target_endpoint, err_from_handler_for_proxy_grpc)
						time.Sleep(5 * time.Second)
						continue
					}
					break
				}

				proxy_grpc_url := _self.Configuration.Get("controller.apiservice.proxy.grpc.url").(string)

				mux.Handle(proxy_grpc_url+"/", http.StripPrefix(proxy_grpc_url, _self.AuthenticationBasic.EnableAuthenticationBasicForHttpHandler(ctx, "admin", handler_for_proxy_grpc)))

				log.Printf("Starting proxy gRPC-UI service at http://%+v%+v => grpc://%+v \n", endpoint, proxy_grpc_url, proxy_grpc_target_endpoint)
			}()

			log.Fatal(http.ListenAndServe(endpoint, mux))
		}
	}()
}
