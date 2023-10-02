{% args IO_pins %}

{% for i,IO_pin in enumerate(IO_pins) %}

    <h3>Pin {{i}}</h3>

    <div>
        <label for="pin_{{i}}">Label</label>
        <input type="text" id="pin_{{i}}" name="label" required
            minlength="3" maxlength="20" size="10" value="{{ IO_pin.label }}" />
    </div>

    <div>
        <label for="pin_type_{{i}}">Type</label>
        <input type="text" name="pin_type" id="pin_type_{{i}}" list="defaultTypes" value="{{ IO_pin.pin_type }}"/>
        <datalist id="defaultTypes">
          <option value="led">led</option>
          <option value="digital">digital</option>
          <option value="button">button</option>
          <option value="analog">analog</option>
          <option value="I2C-RX">I2C-RX</option>
          <option value="I2C-TX">I2C-TX</option>
        </datalist>
    </div>

    <div>
        <label for="pin_Pico_{{i}}">Pico Pin</label>
        <input type=number name="Pico" id="pin_Pico_{{i}}" list="defaultNumbers" value="{{ IO_pin.Pico }}"/ >
        <datalist id="defaultNumbers">
          <option value="4"></option>
          <option value="5"></option>
          <option value="6"></option>
          <option value="7"></option>
          <option value="9"></option>
          <option value="10"></option>
          <option value="11"></option>
          <option value="12"></option>
          <option value="14"></option>
          <option value="15"></option>
          <option value="16"></option>
          <option value="17"></option>
          <option value="19"></option>
          <option value="20"></option>
          <option value="21"></option>
          <option value="22"></option>
          <option value="24"></option>
          <option value="25"></option>
          <option value="26"></option>
          <option value="27"></option>
          <option value="29"></option>
        </datalist>
    </div>

{% endfor %}
