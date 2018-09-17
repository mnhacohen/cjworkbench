// Simple wrapper over HTML <select>
import React from 'react'
import PropTypes from 'prop-types'

export default class RadioParam extends React.PureComponent {
  onChange = (evt) => {
    var idx = evt.target.value;
    this.props.onChange(idx);
  }

  isChecked = (idx) => {
    return idx == this.props.selectedIdx
  }

  render() {
    var items = this.props.items.split('|');
    var itemDivs = items.map( (name, idx) => {
      const strIdx = idx.toString()
      return (
        <label className='t-d-gray content-3'>
          <input
            className='radio-button'
            name={name}
            type='radio'
            value={strIdx}
            checked={this.isChecked(strIdx)}
            onChange={this.onChange}
            disabled={this.props.isReadOnly}
          />
          {name}
        </label>
      )});

    return (
      <div className='button-group'>
        {itemDivs}
      </div>
    );
  }
}

RadioParam.propTypes = {
  name:         PropTypes.string.isRequired,
  items:        PropTypes.string,  // like 'Apple|Banana|Kitten'
  selectedIdx:  PropTypes.number,
  isReadOnly:   PropTypes.bool,
  onChange:     PropTypes.func     // called with index of selected item
};
