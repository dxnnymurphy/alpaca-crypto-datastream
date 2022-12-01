package configuration

type Configuration interface {
	Get(configuration_key string) (configuration_value interface{})
	Set(configuration_key string, configuration_value interface{})
}
