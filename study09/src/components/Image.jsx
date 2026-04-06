import Avatar1 from "@assets/img_avatar1.png"
import Avatar2 from "@assets/img_avatar2.png"

const Image = ({check, className, alt}) => {
  const getImage = () => check ? Avatar1 : Avatar2
  return <img src={getImage()} className={className} alt={alt} />
}

export default Image