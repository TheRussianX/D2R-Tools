#Import/Export script for Diablo II: Resurrected .texture format
#by Jayn23 at Xentax fourm; fixed by Google Gemini for some black ORM maps and with Blue channel for normal maps


from inc_noesis import *
import math

TEX_TYPE = 'Default'
#TEX_TYPE = 'DXT1'
#TEX_TYPE = 'DXT5'
#TEX_TYPE = 'BC4'
#TEX_TYPE = 'RGBA32'
SWIZZLE = False

def registerNoesisTypes():
    handle = noesis.register("Diablo II: Resurrected texture", ".texture")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadRGBA(handle, noepyLoadRGBA)
    noesis.setHandlerWriteRGBA(handle, textureWriteRGBA)
    noesis.addOption(handle, '-DXT1', "Set Output Format DXT1", 0)
    noesis.addOption(handle, '-DXT5', "Set Output Format DXT5", 0)
    noesis.addOption(handle, '-BC4', "Set Output Format BC4", 0)
    noesis.addOption(handle, '-RGBA32', "Set OUtput Format RGBA32", 0)
    noesis.addOption(handle, '-SWIZZLE', "Swap red and green channels for normal maps", 0)
    noesis.logPopup()
    return 1
    

def noepyCheckType(data):
    '''Verify that the format is supported by this plugin. Default yes'''
    return 1
 
 
class MipInfo :
      
      def __init__(self):
            self.start = 0
            self.size = 0

def reconstruct_normal_blue(data, width, height):
    data = bytearray(data)
    num_pixels = width * height
    
    for i in range(num_pixels):
        idx = i * 4
    
        nx = (data[idx + 3] / 255.0) * 2.0 - 1.0
        ny = (data[idx + 1] / 255.0) * 2.0 - 1.0
        

        nz_sqr = 1.0 - (nx * nx) - (ny * ny)
        nz = math.sqrt(max(0.0, nz_sqr)) # max previne erori din cauza aproximărilor float
        
        r_final = int(((nx + 1.0) / 2.0) * 255.0)
        g_final = int(((ny + 1.0) / 2.0) * 255.0)
        b_final = int(((nz + 1.0) / 2.0) * 255.0)
        

        data[idx]     = r_final  # Red (X)
        data[idx + 1] = g_final  # Green (Y)
        data[idx + 2] = b_final  # Blue (Z)
        data[idx + 3] = 255      # Alpha
        
    return data

def noepyLoadRGBA(data, texList):
        
        MipData = []
        imgData = []
        texFmt = noesis.NOESISTEX_RGBA32

        f = NoeBitStream(data, NOE_LITTLEENDIAN)
        MagicValue = f.readUInt()
        Type = f.readUShort()
        print("Format Type detectat:", Type)
        unk = f.readUShort()
        imgWidth = f.readUInt()
        imgHeight = f.readUInt()
        depth = f.readUInt()
        
        # layoutType and layoutData
        f.seek(8, 1)
        MipLevels = f.readUInt()
        Channel_Count = f.readUInt()

        for i in range(MipLevels):
            Temp = MipInfo()
            Temp.size = f.readUInt()
            Current = f.tell() 
            Temp.start = f.readUInt()
            Temp.start += Current
            MipData.append(Temp)


        for Map in MipData:
            f.seek(Map.start, 0)
            imgData += f.readBytes(Map.size)

        data = bytearray(imgData)

        if Type == 31: # RGBA32
            texFmt = noesis.NOESISTEX_RGBA32
        elif Type == 57 or Type == 58: # DXT1  
            texFmt = noesis.NOESISTEX_DXT1
        elif Type == 61 or Type == 62: # DXT5   
            
            data = rapi.imageDecodeDXT(data, imgWidth, imgHeight, noesis.FOURCC_DXT5)

            tex_name = rapi.getInputName().lower()
            if "_nrm" in tex_name:
                
                data = reconstruct_normal_blue(data, imgWidth, imgHeight)
            else:


                data = bytearray(data)
            

                for i in range(3, len(data), 4):
                    data[i] = 255
            texFmt = noesis.NOESISTEX_RGBA32
        elif Type == 63: # BC4 / BC7
            try:

                data = rapi.imageDecodeDXT(data, imgWidth, imgHeight, noesis.FOURCC_BC7)
                data = bytearray(data)
                for i in range(3, len(data), 4):
                    data[i] = 255
                texFmt = noesis.NOESISTEX_RGBA32
            except:

                data = rapi.imageDecodeDXT(data, imgWidth, imgHeight, noesis.FOURCC_BC4)
                texFmt = noesis.NOESISTEX_RGBA32

        tex = NoeTexture(rapi.getInputName(), imgWidth, imgHeight, data, texFmt)
        texList.append(tex)

        return 1






            
            
def textureWriteRGBA(data, width, height, bs):
    
    MAGIC = 0x2845443C
    MipLevels = 0
    mipWidth = width
    mipHeight = height
    TextureData = []
    AllData = bytearray()
    Sum = 0
    

    if TEX_TYPE == 'DXT1' or noesis.optWasInvoked('-DXT1'):
        type = 57
        texFmt = noesis.NOE_ENCODEDXT_BC1
    elif TEX_TYPE == 'DXT5' or noesis.optWasInvoked('-DXT5'):
        type = 61
        #texFmt = noesis.NOE_ENCODEDXT_BC3
        #texFmt = noesis.FOURCC_BC3
        texFmt = noesis.FOURCC_DXT5
    elif TEX_TYPE == 'BC4' or noesis.optWasInvoked('-BC4'):
        type = 63
        texFmt = noesis.NOE_ENCODEDXT_BC4
    elif TEX_TYPE == 'RGBA32' or noesis.optWasInvoked('-RGBA32'):
        type = 31
        texFmt = noesis.NOESISTEX_RGBA32
    else:
        print('Unsupported format')
        return 0

    #Normal map the swap green and red channels
    if  noesis.optWasInvoked('-SWIZZLE') or SWIZZLE:
        data = rapi.imageNormalSwizzle(data, width, height, 1, 1, 0)

    if type == 31:
        imgData = rapi.imageEncodeRaw(data, width, height, "r8 g8 b8 a8")
        MipSize = len(imgData)
        TextureData.append(imgData)
        HeaderSize = 44
        
    elif type == 57 or type == 61 or type == 63:

        while mipWidth > 4 or mipHeight > 4:
            mipData = rapi.imageResample(data, width, height, mipWidth, mipHeight)
            imgData = rapi.imageEncodeDXT(mipData, 4, mipWidth, mipHeight, texFmt)
            TextureData.append(imgData)
            MipSize = len(imgData)
            
            if mipWidth > 4:
                mipWidth //= 2
                
            if mipHeight > 4:
                mipHeight //= 2
            
    HeaderSize = 36 + 8 *len(TextureData)
    bs.writeUInt(MAGIC)
    bs.writeUShort(type)
    MipUnk = 258 + (len(TextureData) - 1) * 256
    bs.writeUShort(MipUnk)
    bs.writeUInt(width)
    bs.writeUInt(height)
    #depth
    bs.writeUInt(0x1)
    #layoutType and layoutData
    bs.writeUInt64(0x0)
    MipLevels = len(TextureData)
    bs.writeUInt(MipLevels)
    bs.writeUInt(0x4)
    
    for i in range(MipLevels):
        bs.writeUInt(len(TextureData[i]))
        Current = bs.tell()
        MipStartLocation = HeaderSize - Current + Sum
        Sum += len(TextureData[i])
        bs.writeUInt(MipStartLocation)
        AllData += TextureData[i]
      
    bs.writeBytes(AllData)
    
    return 1