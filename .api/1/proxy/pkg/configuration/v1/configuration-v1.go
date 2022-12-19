package configurationv1

import (
	"context"
	"log"
	"os"
	"reflect"
	"strings"

	"gopkg.in/yaml.v2"

	"dxnnymurphy.io/datastream/pkg/resource"
)

type ConfigurationV1 struct {
	_Configuration map[string]interface{}
}

func NewConfigurationV1(ctx context.Context) (instance *ConfigurationV1) {
	instance = &ConfigurationV1{
		_Configuration: make(map[string]interface{}),
	}

	func() {
		var configuration_application_yml map[interface{}]interface{}
		if err0 := yaml.Unmarshal([]byte(resource.ConfigApplicationYml), &configuration_application_yml); err0 != nil {
			log.Fatalf("Failed to unmarshal resource/config/application.yml - %+v", err0)
		}

		var _LoadInstanceConfiguration func(configuration0 map[interface{}]interface{}, key_prefix string)
		_LoadInstanceConfiguration = func(configuration0 map[interface{}]interface{}, key_prefix string) {
			for configuration_key, configuration_value := range configuration0 {
				prefixed_configuration_key := key_prefix + configuration_key.(string)
				if reflect.ValueOf(configuration_value).Kind() == reflect.Map {
					key_prefix_next := prefixed_configuration_key + "."
					_LoadInstanceConfiguration(configuration_value.(map[interface{}]interface{}), key_prefix_next)
				} else {
					instance._Configuration[prefixed_configuration_key] = configuration_value
				}
			}
		}

		_LoadInstanceConfiguration(configuration_application_yml, "")
		//log.Printf("Loaded config/application.yml - %+v", instance._Configuration)
	}()

	func() {
		for configuration_key, _ := range instance._Configuration {
			environment_key := "KCDE_API_1_PROXY_" + strings.Replace(strings.ToUpper(configuration_key), ".", "_", -1)
			environment_value, ok := os.LookupEnv(environment_key)
			if ok {
				instance._Configuration[configuration_key] = environment_value
			}
		}

		//log.Printf("Overrided configuration from environment variables - %+v", instance._Configuration)
	}()

	return instance
}

func (_self *ConfigurationV1) Get(configuration_key string) (configuration_value interface{}) {
	configuration_value = _self._Configuration[configuration_key]
	return configuration_value
}

func (_self *ConfigurationV1) Set(configuration_key string, configuration_value interface{}) {
	_self._Configuration[configuration_key] = configuration_value
}
