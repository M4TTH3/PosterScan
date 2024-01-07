import Greet from "@/components/Greet";
import ShowUsersName from "@/components/ShowUsersNames";
import TestSharp from "@/components/TestSharp"

export default async function Home() {

  return (
    <>
      <Greet />
      <ShowUsersName />
      <div className="border flex mx-auto justify-center p-4 align-center">center a div why does it not update correctly </div>
      <TestSharp />
    </>
  )
}
