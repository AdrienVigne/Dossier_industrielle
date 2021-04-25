import Peda.gateway.gateway as gate_peda

if __name__ == '__main__':
    g = gate_peda.Gateway()
    g.clientMqtt.Debug = True
    g.run()

