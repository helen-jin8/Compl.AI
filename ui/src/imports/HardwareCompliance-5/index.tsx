import svgPaths from "./svg-rxv5osztjt";

function Send({ className }: { className?: string }) {
  return (
    <div className={className || "overflow-clip relative size-[24px]"} data-name="send">
      <div className="absolute inset-[16.67%_8.33%_16.67%_12.5%]" data-name="icon">
        <svg className="absolute block inset-0 size-full" fill="none" height="16" preserveAspectRatio="none" viewBox="0 0 19 16" width="19">
          <path d={svgPaths.p38ee5a80} fill="#1D1B20" id="icon" />
        </svg>
      </div>
    </div>
  );
}

export default function HardwareCompliance() {
  return (
    <div className="bg-gradient-to-b from-[rgba(17,75,138,0.45)] relative size-full to-[rgba(117,185,255,0.45)]" data-name="Hardware Compliance">
      <p className="[word-break:break-word] absolute font-['Gloock:Regular',sans-serif] h-[166.5px] leading-[normal] left-[47.27px] not-italic text-[50px] text-white top-[69.71px] w-[425.499px]">compl.ai</p>
      <div className="absolute bg-white border border-[#1f1a1a] border-solid h-[1217.714px] left-[47.27px] rounded-[10px] top-[189.07px] w-[325.675px]" />
      <p className="[word-break:break-word] absolute font-['Glegoo:Regular',sans-serif] h-[44.5px] leading-[normal] left-[86.6px] not-italic text-[#040404] text-[24px] top-[392.5px] w-[247.029px]">Project summary</p>
      <div className="absolute bg-white border border-[#1f1a1a] border-solid h-[1217.714px] left-[414.54px] rounded-[10px] top-[189.07px] w-[1084.125px]" />
      <p className="[word-break:break-word] absolute font-['Glegoo:Regular',sans-serif] h-[44.5px] leading-[normal] left-[86.6px] not-italic text-[#040404] text-[24px] top-[236.21px] w-[247.029px]">Follow Up</p>
      <p className="[word-break:break-word] absolute font-['Glegoo:Bold',sans-serif] h-[44.5px] leading-[normal] left-[86.6px] not-italic text-[#040404] text-[24px] top-[457.85px] w-[247.029px]">Standards</p>
      <p className="[word-break:break-word] absolute font-['Glegoo:Regular',sans-serif] h-[44.5px] leading-[normal] left-[86.6px] not-italic text-[#040404] text-[24px] top-[522.67px] w-[247.029px]">Labs</p>
      <p className="[word-break:break-word] absolute font-['Glegoo:Regular',sans-serif] h-[145.065px] leading-[normal] left-[472.77px] not-italic text-[#5b5b5b] text-[24px] top-[250.71px] w-[833.352px]">The following standards are necessary for testing</p>
      <div className="absolute bg-[#d9d9d9] h-[82.427px] left-[476.92px] rounded-[10px] top-[340.07px] w-[829.2px]" />
      <div className="absolute bg-[#d9d9d9] h-[85.145px] left-[476.92px] rounded-[10px] top-[459.78px] w-[829.2px]" />
      <div className="absolute bg-[#d9d9d9] h-[85.145px] left-[476.92px] rounded-[10px] top-[589.64px] w-[829.2px]" />
      <div className="absolute bg-[#d9d9d9] h-[85.145px] left-[476.92px] rounded-[10px] top-[719.5px] w-[829.2px]" />
      <div className="absolute bg-[#fffefe] border border-black border-solid h-[85.145px] left-[472.77px] rounded-[10px] top-[1201.28px] w-[833.353px]" />
      <p className="[word-break:break-word] absolute font-['Glegoo:Regular',sans-serif] h-[39.458px] leading-[normal] left-[476.92px] not-italic text-[20px] text-black top-[1298.03px] w-[424.758px]">gets back to you in 2-3 hours</p>
      <p className="[word-break:break-word] absolute font-['Glegoo:Regular',sans-serif] h-[39.458px] leading-[normal] left-[496.29px] not-italic text-[20px] text-black top-[1226.19px] w-[424.758px]">ask an expert</p>
      <Send className="absolute left-[1226px] overflow-clip size-[53px] top-[1212.65px]" />
    </div>
  );
}