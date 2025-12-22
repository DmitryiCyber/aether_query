package goja

type ModuleLoader struct {
	modules map[string]string
}

func NewModuleLoader() *ModuleLoader {
	return &ModuleLoader{
		modules: make(map[string]string),
	}
}

func (ml *ModuleLoader) RegisterModule(name string, code string) {
	ml.modules[name] = code
}

func (ml *ModuleLoader) GetModule(name string) (string, bool) {
	code, exists := ml.modules[name]
	return code, exists
}
