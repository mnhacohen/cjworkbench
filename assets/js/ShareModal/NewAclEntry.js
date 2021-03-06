import React from 'react'
import PropTypes from 'prop-types'

export default class NewAclEntry extends React.PureComponent {
  static propTypes = {
    onCreate: PropTypes.func.isRequired, // func(email, canEdit) => undefined
  }

  emailRef = React.createRef()

  // No state: we're using uncontrolled components, because the logic is so
  // simple. If you're adding new features, consider switching to controlled
  // components.
  // https://reactjs.org/docs/uncontrolled-components.html

  onSubmit = (ev) => {
    // onSubmit() is only called after <form> passes validation -- meaning
    // email address is valid
    const email = this.emailRef.current.value

    this.props.onCreate(email, false)

    // Reset the input, so the user can enter another email. (It should retain
    // focus.)
    this.emailRef.current.value = ''

    ev.preventDefault() // don't let the browser change URL etc.
    ev.stopPropagation()
  }

  render () {
    // Uncontrolled form -- we'll use HTML5 validation, with its :valid and
    // :invalid classes.
    return (
      <form className='new-acl-entry input-group' onSubmit={this.onSubmit}>
        <input className='form-control' type='email' name='email' ref={this.emailRef} required placeholder='user@example.org' />
        <div className='input-group-append'>
          <button type='submit' className='btn btn-outline-secondary'>Grant access</button>
        </div>
      </form>
    )
  }
}
